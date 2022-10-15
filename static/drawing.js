var canvas = document.querySelector('.ann-canv');
var context = canvas.getContext("2d");

var colour = "#000000";
var tool = "pen";
var size = 5;
var inStroke = false;
var posLast = { x: 0, y: 0 };
var isDrawing = false;
var useTilt = false;

var strokes = [];
var currstroke = [];
var undone = [];

var EPenButton =
{
    tip: 0x1,		// left mouse, touch contact, pen contact
    barrel: 0x2,		// right mouse, pen barrel button
    middle: 0x4,		// middle mouse
    eraser: 0x20		// pen eraser button
};

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

document.addEventListener('resize', (event) => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

function clear() {
    strokes = [];
    currstroke = [];
    undone = [];
    context.clearRect(0, 0, canvas.width, canvas.height);
}

function midpoint(p1, p2) {
    return {
        x: p1.x + (p2.x - p1.x) / 2,
        y: p1.y + (p2.y - p1.y) / 2
    };
}

function draw_canvas() {
    context.canvas.width = context.canvas.width;
    for (stroke of strokes) {
        context.fillStyle = stroke.colour;
        context.strokeStyle = stroke.colour;
        for (i = 0; i < stroke.stroke.length - 1; i++) {
            sx = stroke.stroke[i]['x']
            sy = stroke.stroke[i]['y']
            sw = stroke.stroke[i]['width']
            sx1 = stroke.stroke[i+1]['x']
            sy1 = stroke.stroke[i+1]['y']
            sw1 = stroke.stroke[i+1]['width']

            context.lineWidth = sw1;
            context.beginPath();
            context.lineCap = "round";
            context.moveTo(sx, sy);

            var midPoint = midpoint(stroke.stroke[i], stroke.stroke[i+1]);
            context.quadraticCurveTo(sx, sy, midPoint.x, midPoint.y);

            context.lineTo(sx1, sy1);
            context.stroke();

            //context.beginPath();
            //context.moveTo(sx - sw / 2, sy - sw / 2);
            //context.lineTo(sx1 - sw1 / 2, sy1 - sw1 / 2);
            //context.lineTo(sx1 + sw1 / 2, sy1 + sw1 / 2);
            //context.lineTo(sx + sw / 2, sy + sw / 2);
            //context.closePath();
            //context.fill();
            //context.stroke();
        }
    }
}

function set_colour(el) {
    colour = el.dataset.colour;
    document.querySelectorAll('.pen-colour').forEach(pc => {
        pc.classList.remove('selected');
    });
    el.classList.add('selected');
}

function set_tool(el) {
    tool = el.dataset.tool;
    document.querySelectorAll('.pen-tool').forEach(pc => {
        pc.classList.remove('selected');
    });
    el.classList.add('selected');
}

function set_size(el) {
    size = parseInt(el.dataset.size);
    document.querySelectorAll('.pen-size').forEach(pc => {
        pc.classList.remove('selected');
    });
    el.classList.add('selected');
}

window.addEventListener('load', function () {
    var events = [
        'MSPointerDown', 'MSPointerUp', 'MSPointerCancel', 'MSPointerMove', 'MSPointerOver', 'MSPointerOut', 'MSPointerEnter', 'MSPointerLeave', 'MSGotPointerCapture', 'MSLostPointerCapture', 'touchstart', 'touchmove', 'touchend', 'touchenter', 'touchleave', 'touchcancel', 'mouseover', 'mousemove', 'mouseout', 'mouseenter', 'mouseleave', 'mousedown', 'mouseup', 'focus', 'blur', 'click', 'webkitmouseforcewillbegin', 'webkitmouseforcedown', 'webkitmouseforceup', 'webkitmouseforcechanged'
    ];

    var pointerEvents = [
        'pointerdown', 'pointerup', 'pointercancel', 'pointermove', 'pointerover', 'pointerout', 'pointerenter', 'pointerleave', 'gotpointercapture', 'lostpointercapture'
    ];

    draw_event = evt => {

    }

    function draw_pointerevent(evt) {
        //console.log(evt.type);
        var canvasRect = canvas.getBoundingClientRect();
        var pos = {
            x: evt.clientX - canvasRect.left,
            y: evt.clientY - canvasRect.top,
        }
        var pressure = evt.pressure;
        var buttons = evt.buttons;
        var tilt = { x: evt.tiltX, y: evt.tiltY };
        var rotate = evt.twist;

        if (evt.pointerType) {
            switch (evt.pointerType) {
                case "touch":
                pressure = 0.5;
                break;

                case "pen":
                break;

                case "mouse":
                pressure = 0.5;
                break;
            }
            
            context.strokeStyle = colour
            context.lineWidth = pressure * size;

            switch (evt.type) {
                case "pointerdown":
                    isDrawing = true;
                    posLast = pos;
                    stroke = [posLast];
                    break;

                case "pointerup":
                    isDrawing = false;
                    strokes.push({stroke: stroke, colour: colour});
                    stroke = [];
                    draw_canvas();
                    break;

                case "pointermove":
                    if (!isDrawing) {
                        return;
                    }

                    else if (pressure > 0) {
                        if (tool == "pen") {
                            context.beginPath();
                            context.lineCap = "round";
                            context.moveTo(posLast.x, posLast.y);

                            // Draws Bezier curve from context position to midPoint.
                            var midPoint = midpoint(posLast, pos);
                            context.quadraticCurveTo(posLast.x, posLast.y, midPoint.x, midPoint.y);

                            // This lineTo call eliminates gaps (but leaves flat lines if stroke
                            // is fast enough).
                            context.lineTo(pos.x, pos.y);
                            context.stroke();
                            stroke.push({x: pos.x, y: pos.y, width: pressure * size});
                        }
                    }

                    posLast = pos;
                    break;

                case "pointerenter":
                    document.body.style.cursor = "crosshair";
                    break;

                case "pointerleave":
                    document.body.style.cursor = "default";
                    break;

                default:
                    break;
            }
        }
    }


    if (window.PointerEvent) {
        for (ev of pointerEvents) {
            canvas.addEventListener(ev, draw_pointerevent, false);
        }
    }
    else {
        //for (ev of events) {
        //    canvas.addEventListener(ev, draw_event, false);
        //}
        alert("Your browser does not support pointer events. Support for non-pointer APIs has not been implemented yet.")
    }
}, true);

document.onkeydown = function (e) {
    if (document.querySelector('.drawing-controls').style.visibility == 'visible') {
        if (e.ctrlKey) {
            if (e.key == 'z') {
                if (strokes.length > 0) {
                    undone.push(strokes.pop());
                    console.log('undoing')
                    draw_canvas();
                }
            }
            else if (e.key == 'y') {
                if (undone.length > 0) {
                    strokes.push(undone.pop());
                    console.log('redoing')
                    draw_canvas();
                }
            }
        }
    }
}
