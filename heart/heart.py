import gizeh as gz 
import numpy as np 
import moviepy.editor as mpy 

dur = 1.3 # duration

s =  500 # frame size
center = [s/2, s/2]


### consts for background circles
baseRadius = 50
numOfCircles = 7
ratio = baseRadius*2


### consts for heart arcs
pi = np.pi
hpi = pi/2
ofst = 0.7
ofstRadian = -hpi-ofst
radius = 70
arcX = np.cos(ofstRadian) * radius + ofst   #'+ ofst' to get rid of a slight inaccuracy
arcY = np.sin(ofstRadian) * radius 

### triangle points
A = (220, center[0]-100)
C = (A[0], center[0]+100)
B = (A[0]*0.64, (C[1]+A[1])/2) # B[0] picked randomly
points = [A, B, C]


black = (0, 0, 0)
red = np.array([255, 0, 0])
opacRed = (255,0,0, .15)
white = (255, 255, 255)


def easeOut(m):
    m -= 1
    return 1 + m ** 5

def easeIn(m):
    return m ** 5


def animateScale(progress, pipeline: list) -> float:
    """
    Take stage from pipeline, calculate stage progress and pass it to easing
    Return the scale value for the current progress 

    // Pipeline is an array of dicts, each dict is a stage of animation //
    """
    
    stageEnd = 0
    for ind, stage in enumerate(pipeline):
        if ind >= 1:
            stage["initScale"] = pipeline[ind-1]["finScale"]      
        stageProgress = (progress - stageEnd) / (stage["dur"])
        stageEnd += stage["dur"]                
        if progress < stageEnd:
            modProgress = stage["modify_progress"](stageProgress)
            scale = stage["initScale"] + (stage["finScale"] - stage["initScale"]) * modProgress
            return scale


# The necessary values for each stage are 
# easing func to use, duration and final scale
pipeline = [ 
    {
        "modify_progress": easeIn,
        "dur": 0.5 / 3,
        "initScale": 1,
        "finScale": 1.5,
    },
    {
        "modify_progress": easeOut,
        "dur": 0.5 / 3, 
        "finScale": 1.25,
    },
    {
        "modify_progress": easeIn,
        "dur": 0.5 / 3,
        "finScale": 1.5,
    },
    {
        "modify_progress": easeOut,
        "dur": 0.5,
        "finScale": 1,
    },
]



def createHeart(stroke, stroke_width, fill=None):

    line = gz.polyline(points=points, stroke_width=stroke_width,
                        stroke=stroke, fill=red)  
    arc1 = gz.arc(r=radius, a1=ofstRadian, a2=-ofstRadian, stroke=stroke, stroke_width = stroke_width,
                    xy=[A[0]-arcX, A[1]-arcY], fill=red)  
    arc2 = gz.arc(r=radius, a1=ofstRadian, a2=-ofstRadian, stroke=stroke, stroke_width = stroke_width,
                    xy=[C[0]-arcX, C[1]+arcY], fill=red)   

    return gz.Group([line, arc1, arc2])


def make_frame(t):
    surface = gz.Surface(s, s, bg_color=black)
    progress = t / dur

    circles = []
    prevRadius = baseRadius
    for i in range(numOfCircles):
        r = baseRadius if i == 0 else prevRadius + ratio 
        prevRadius = r
        modRadius = r - ratio * 2 * progress
        circles.append(gz.circle(modRadius, stroke=(255,0,0, .5), stroke_width=10, xy=center))
        circles.append(gz.circle(modRadius*.9, stroke=(255,0,0, .2), stroke_width=30, xy=center))
    circles.reverse()
    grCircles = gz.Group(circles)
    grCircles.draw(surface)
    
    stageScale = animateScale(progress, pipeline)
    rand = np.random.randint(10, 30)

    redHeart = createHeart(stroke=red, stroke_width=3, fill=red).rotate(-hpi, 
                center=center).scale(stageScale, center=center)

    shakingHeart = createHeart(stroke=opacRed, stroke_width=rand).rotate(-hpi + np.random.randint(-1, 1) / 20, 
                center=center).scale(0.05+stageScale, center=center)

    redHeart.draw(surface)
    shakingHeart.draw(surface) 

    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=dur)
clip.write_gif("heart.gif", fps=30, opt="OptimizePlus")
