// Where is the circle
var x, y;
var x2, y2;
var color_of_building;
var buildings, robots,lights,light2;
var step;
var light_status;
var robot_coorinator = [];
var robots_on_map = [];
var robot_obj;
var  array_traffic_light;
var  array_traffic_light2;
var reported_ajax_error = false;  
var traffic_lightcolor;
var traffic_set_gui;
var reported_ajax_call = false;
function setup() {

 

  //createCanvas(w, h, [renderer])
  createCanvas(720, 470);
 

  // width and height of the canvas
  x = width / 3;
  y = height;
  color_of_building = color(255, 0, 0);
  //step of the robot(how quick the robot goes)
  step = 5;

  //building objects
  var blackRectangle = {x:250,y:30,width:200,height:80,colour:color(0,0,0)};
  var brightGreenRectangle = {x:500,y:30,width:180,height:80,colour:color(188, 251, 0)};
  var yellowRectangle = {x:500, y:150,width:180,height:215,colour:color(254, 251, 0)};
  var greyRectangle1 = {x:400, y:150,width:50,height:150,colour:color(159, 171, 179)};
  var greyRectangle2 = {x:250,y:260,width:150,height:40,colour:color(159, 171, 179)};
  var purpleRectangle = {x:250, y:330,width:210,height:30,colour:color(159, 76, 179)};
  var blueRectangle = {x:50, y:30,width:150,height:170,colour:color(57, 76, 179)};
  var darkRedRectangle = {x:50, y:260,width:150,height:95,colour:color(176, 5, 45)};


  //ajax request to dummy for robot (coordinates)
  function fetch_ajax_robot(){
    $.ajax({url: "http://127.0.0.1:9999/robot", success: function(result){
      //127.0.0.1:9999/traffic
      //populating the array 
      check_robot_on_map(result);
      robot_coorinator = result;
    }});
  }

  //ajax request to dummy robot
  $(document).ready(function(){

    //fectching ajax for robot every 100 millisecond second 
    //setInterval(fetch_ajax_robot,100);

    //fectching ajax for traffic  every 100 millisecond second 
    // fetch_ajax_traffic_lights();
    setInterval(fetch_ajax_traffic_lights,100);
    document.getElementById("trafficLight").addEventListener("click", show_traffic_light);
    //fectching ajax for robot every 100 millisecond second 
    // setTimeout(populate_select_tag(array_traffic_light), 1000);
    fetch_ajax_traffic_lights_gui();
  });

  //array containing all the buildings
  buildings = [blackRectangle, brightGreenRectangle, yellowRectangle, greyRectangle1, greyRectangle2, purpleRectangle, blueRectangle, darkRedRectangle];
}

// ajax request to dummy traffics coordinates for traffic light drawing (REQUESTED EVERY 100 MILLISECOND)
function fetch_ajax_traffic_lights(){
    url = "http://127.0.0.1:9999/traffic";
    $.ajax(url, {
      "type": "GET"
  })
  //error handling
  .done(function (data, textStatus, jqXHR) {
      array_traffic_light = data;
      if (reported_ajax_call != true) {
        // populate_select_tag(data);
        console.log("populate_select_tag");
        reported_ajax_call = true;
      }

  })
  .fail(function (jqXHR, textStatus, errorThrown) {
    // console.log(errorThrown);
      if (reported_ajax_error != true) {
        console.log("Ajax error, possibly server is not working.");
        reported_ajax_error = true;
      }
  })
  .always(function(jqXHR, textStatus, errorThrown) {
    // console.log(textStatus);
  })

}

// ajax request to dummy traffics coordinates for traffic light GUI  name 
function fetch_ajax_traffic_lights_gui(){
  url = "http://127.0.0.1:9999/traffic";
  $.ajax(url, {
    "type": "GET"
})

.done(function (data, textStatus, jqXHR) {
    array_traffic_light2 = data;
    populate_select_tag(array_traffic_light2);
})
.fail(function (jqXHR, textStatus, errorThrown) {
  // console.log(errorThrown);
    if (reported_ajax_error != true) {
      console.log("Ajax error, possibly server is not working.");
      reported_ajax_error = true;
    }
})
.always(function(jqXHR, textStatus, errorThrown) {
  // console.log(textStatus);
})

}





function draw() {
   
  
   //defining the color
   background(200);
   //horizontal line 
   hori_dash_line(230,200,80);
   //horizontal line 
   hori_dash_line(15,700,10);
   //horizontal line 
   hori_dash_line(315,450,275);
   //horizontal line 
   hori_dash_line(380,width,0);
   //horizontal line 
   hori_dash_line(130,700,275);     

   // vertical dashed lines
   stroke(0);
   //vert_dash_line(x,start_pointY ,end_pointY)
   vert_dash_line(225,350,60);

   // vertical dashed lines
   stroke(0);
   vert_dash_line(22,350,60);
   // vertical dashed lines
	 stroke(0);
   vert_dash_line(480,350,60);
   // vertical dashed lines
	 stroke(0);
   vert_dash_line(700,350,60);
  
   // genrate Buildings
   generateBuildings(buildings);
  
   //generate traffic light
    if (array_traffic_light !== undefined){
      generate_traffic_lights(array_traffic_light);
    }
  
   //generate robot
   generate_robot(robot_coorinator);
  
   // roundabout 
   stroke(50);
   // roundabout color
   fill(color(0,0,0));
   var xaxis_5 = 330;
   var yaxis_5 =  200;
   ellipse(xaxis_5, yaxis_5, 60,60);


  //console.log(traffic_set_gui);
  //set traffic light gui
  /// traffic light color
   traffic_set_gui = color(204, 102, 0);
  generate_traffic_gui(traffic_set_gui);
  
 }

 // vertical dash line
 function vert_dash_line(x,start_pointY ,end_pointY) {
    var   dash_length = 20;
    var   gap_length = 10;
    var   currY = start_pointY;
    
    while ((currY + dash_length) > end_pointY){ 
		line(x,currY,x, (currY - dash_length));
		currY =	currY - dash_length - gap_length;
	}
 }
 // horizon  dash line
 function hori_dash_line(y,start_pointX ,end_pointX) {
	 var   currX = start_pointX;
	 var   dash_length = 20;
	 var   gap_length = 10;
   while ((currX + dash_length) > end_pointX){ 
		    line(currX,y, (currX - dash_length), y);
		    currX =	currX - dash_length - gap_length;
	  }
 }

 //controlling robot with arrow keys
//  function keyPressed() {
//   if(keyCode == UP_ARROW) {
//     move_robot(robots[0],"up");
//   } else if (keyCode == DOWN_ARROW) {
//     move_robot(robots[0],"down");
//   } else if (keyCode == LEFT_ARROW) {
//     move_robot(robots[0],"left");
//   }else if (keyCode = RIGHT_ARROW){
//     move_robot(robots[0],"right");
//   }
//   return 0;
// }

//generate buildings
function generateBuildings(recs){

  recs.forEach(function(rec) {
    fill(rec.colour);
    rect(rec.x, rec.y, rec.width, rec.height);
  });

}

//generate robots
function generate_robot(objs){

  objs.forEach(function(obj) {   
    ellipseMode(CENTER);
    fill(color(0,0,255));
    stroke(50);
    ellipse(obj.x,obj.y,24,24);
   });
   
}


function generate_traffic_gui(traffic_gui_color){ 
    ellipseMode(CENTER);
    fill(traffic_gui_color);
    stroke(50);
    ellipse(50,450,25,25);
}



//write a function that take a robot object and takes a direction
// function move_robot(robot,direction,){
//   var valid_move = true;
//   //loop to go throught the building array
//   buildings.forEach(function(building){
//     switch (direction){
//       case "up":
//         if(robot.x > building.x && robot.x < (building.x + building.width)) {
//           if ((robot.y - (robot.height / 2) - step) > building.y && (robot.y - (robot.height / 2) - step) < (building.y + building.height)){
//                 valid_move = false;
//           }
//         }
//         break;  
//       case "down":
//         if(robot.x > building.x && robot.x < (building.x + building.width)) {
//           if ((robot.y + (robot.height / 2) + step) > building.y && ((robot.y + (robot.height / 2) + step) < (building.y + building.height))){
//             valid_move = false;
//           }
//         }
//         break;
  
//       case "left":
//       if(robot.y > building.y && robot.y < (building.y + building.height)) {
//         if ((robot.x - (robot.width / 2) - step) > building.x && ((robot.x - (robot.width / 2) - step) < (building.x + building.width))){
//           valid_move = false;
//         }
//       }
//         break;
//       case "right":
//       if(robot.y > building.y && robot.y < (building.y + building.height)) {
//         if ((robot.x + (robot.width / 2) + step) > building.x && ((robot.x + (robot.width / 2) + step) < (building.x + building.width))){
//           valid_move = false;
//         }
//       }
//         break;
//     }
//   });

//   if (valid_move) {
//     switch (direction){
//       case "up":
//         robot.y = robot.y - step;
//         break;

//       case "down":
//         robot.y = robot.y + step;
//         break;
  
//       case "left":
//         robot.x = robot.x - step;
//         break;
  
//       case "right":
//         robot.x = robot.x + step;
//         break;
        
//     }
//   }

// }


//one fucntion that check the name of the array
//intializes an array with 
function check_robot_on_map(robot_list){
  var temp_robot_name = [];

  robot_list.forEach(function(robot) {
    temp_robot_name.push(robot.name);
  });
  var removedRobots = robots_on_map.filter(comparer(temp_robot_name));
  var addedRobots = temp_robot_name.filter(comparer(robots_on_map));
  console.log(removedRobots);
  console.log(addedRobots);

}

//function to compare two arrays
function comparer(otherArray){
  return function(current){
    return otherArray.filter(function(other){
      return other == current
    }).length == 0;
  }
}
//generate traffic lights
function  generate_traffic_lights(lights){
  lights = lights[0];
  for (var l in lights) {
    light = lights[l];
       //console.log(l);
      // console.log(light.x,light.y,light.width,light.height);
      fill(color(200, 254, 0));
      stroke(23);
      light_status = light.status;
      rect(light.x,light.y,light.width,light.height);
  };

}



// populating select tag
 function  populate_select_tag(lights2){
  lights2 = lights2[0];
  console.log("ttt", lights2);
  var x = document.getElementById("trafficLight");
  


  for (var t in lights2) {
    var option = document.createElement("option");
    option.text = t;
    x.add(option);
  };

}

function show_traffic_light(){
  
  var trafficaValue = document.getElementById('trafficLight').value;
  // console.log("light3 " + trafficaValue);
  // console.log(array_traffic_light);
  // compare the json data coming through
  lights_to_display = array_traffic_light[0];
  for (var traffic_light_object in lights_to_display) {
    traffic_light = lights_to_display[traffic_light_object];
    // console.log(traffic_light.status);
    //console.log(traffic_light_object);
    //name match
    if(traffic_light_object == trafficaValue){
      // console.log(traffic_light.status);
        //  matching for the color corresponding 
         if (traffic_light.status == "green"){
              console.log(" change to green");
              //set color to green
              // traffic_set_gui = color(4, 251, 0);
          }
    }else if (traffic_light.status == "red"){
              console.log("change to red");
              //change color to red
              // traffic_set_gui = color(253, 0, 0);
    }else {
       //change color to red
      console.log(" change to black");
      //  traffic_set_gui = color(253, 254, 254);
      
    }
  };
}