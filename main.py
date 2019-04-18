from display import *
from draw import *
from parser import *
from matrix import *
import math
ARG_COMMANDS = [ 'box', 'sphere', 'torus', 'circle', 'bezier', 'hermite', 'line', 'scale', 'move', 'rotate', 'save' ]

def parse_file( fname, edges, polygons, csystems, screen, zbuffer, color ):

    f = open(fname)
    lines = f.readlines()

    clear_screen(screen)
    clear_zbuffer(zbuffer)
    step = 100
    step_3d = 20

    c = 0
    while c < len(lines):
        line = lines[c].strip()
        #print ':' + line + ':'

        if line in ARG_COMMANDS:
            c+= 1
            args = lines[c].strip().split(' ')

        if line == 'push':
            csystems.append( [x[:] for x in csystems[-1]] )

        elif line == 'pop':
            csystems.pop()

        elif line == 'sphere':
            #print 'SPHERE\t' + str(args)
            add_sphere(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult(csystems[-1], polygons)
            draw_polygons(polygons, screen, zbuffer, color)
            polygons = []

        elif line == 'torus':
            #print 'TORUS\t' + str(args)
            add_torus(polygons,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult(csystems[-1], polygons)
            draw_polygons(polygons, screen, zbuffer, color)
            polygons = []

        elif line == 'box':
            #print 'BOX\t' + str(args)
            add_box(polygons,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(csystems[-1], polygons)
            draw_polygons(polygons, screen, zbuffer, color)
            polygons = []

        elif line == 'circle':
            #print 'CIRCLE\t' + str(args)
            add_circle(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(csystems[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif line == 'hermite' or line == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            add_curve(edges,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)
            matrix_mult(csystems[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif line == 'line':
            #print 'LINE\t' + str(args)
            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(csystems[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif line == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(csystems[-1], t)
            csystems[-1] = [x[:] for x in t]


        elif line == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(csystems[-1], t)
            csystems[-1] = [x[:] for x in t]

        elif line == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)

            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(csystems[-1], t)
            csystems[-1] = [x[:] for x in t]

        elif line == 'ident':
            ident(transform)

        elif line == 'apply':
            matrix_mult( transform, edges )
            matrix_mult( transform, polygons )

        elif line == 'clear':
            clear_screen(screen)
            clear_zbuffer(zbuffer)

        elif line == 'display' or line == 'save':
            #clear_screen(screen)
            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
        c+= 1

screen = new_screen()
zbuffer = new_zbuffer()
color = [ 0, 255, 0 ]
edges = []
polygons = []
t = new_matrix()
ident(t)
csystems = [ t ]


parse_file( 'script', edges, polygons, csystems, screen, zbuffer, color )
