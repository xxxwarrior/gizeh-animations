import numpy as np 
import gizeh as gz 
import moviepy.editor as mpy 
from convertedPNG import data

size = 500
dur = 10

pi = np.pi
hpi = pi/2
qpi = hpi/2

blue = (.294, .725, .894) 
pink = (.917, .552, .741) 
yellow = (1, .972, .0823)

points = [-500, 500]
center = [250, 250]


def bounce(m):
    q = 2.25
    u = 0.984375
    v = 7.5625
    w = 0.9375
    x = 2.75
    y = 2.625
    z = 0.75

    if m < 1 / x:
        return v * m * m
    elif m < 2 / x:
        m -= 1.5 / x
        return v * m * m + z
    elif m < 2.5 / x:
        m -= q / x
        return v * m * m + w
    else: 
        m -= y / x
        return v * m * m + u 


def make_frame(t):

    surface = gz.Surface(size, size, bg_color=blue)
    progress = t/dur

    # background lines
    x = 500*progress
    for i in range(10):
        gz.polyline(points=[(0, 500-x-i*50), (x+i*50, 500)], stroke=pink, stroke_width=5).draw(surface)
        gz.polyline(points=[(x+i*50, 0), (500, 500-x-i*50)], stroke=pink, stroke_width=5).draw(surface)
        
    
    scale = bounce(progress)
    randPoints = np.random.randint(500, size=2)
    randR = np.random.randint(100)
    flickeringYellow = (1, .972, .0823, np.random.rand(1))

    # pink 'triangle'
    tr = gz.polyline(points=[(0, 40), (460, 500), (0, 500)], stroke=flickeringYellow, stroke_width=3, fill=pink)
    tr.draw(surface)
    gz.polyline(points=[(0, 500), (230, 270)], stroke=flickeringYellow, stroke_width=3).draw(surface)
    gz.polyline(points=[(230, 270), (230, 500)], stroke=flickeringYellow, stroke_width=3).draw(surface)
    gz.polyline(points=[(230, 270), (0, 270)], stroke=flickeringYellow, stroke_width=3).draw(surface)

    # random squares
    e = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    for i in e:
        if i == progress:
    # if progress%2:
            gz.regular_polygon(r=randR, n=4, xy=randPoints, fill=flickeringYellow).scale(1+scale, center=center).draw(surface) 
            gz.regular_polygon(r=randR, n=4, xy=randPoints, fill=flickeringYellow).scale(1+scale, center=center).draw(surface) 

    
    # really cool rabbit
    img = gz.ImagePattern(image=data, pixel_zero=[110, 150], filter="best", extend="none")

    r = np.random.choice([1, -1, 0], 1, p=[0.1, 0.1, 0.8]) # disturbing rotation 
    circ = gz.circle(r=130, stroke_width=5, stroke=yellow, fill=img, xy=center).rotate((r[0]*qpi)*progress, center=center)
    circ.draw(surface)
    
    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=dur)
clip.write_gif("rabbit.gif", fps=30, opt="OptimizePlus")
