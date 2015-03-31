$(document).ready(function(){
	'use strict';

	var attributes = [];
	var dependencies = [];
	var connections = [];
	var instance = jsPlumb.getInstance();
	var windows = {};

	$('.form_file').validate({
    
        // Specify the validation rules
        rules: {
            file: "required"
        },
        
        // Specify the validation error messages
        messages: {
            file: {
                required: "Campo obligatorio"
            }
        }
    });

	
	$('.form_file').submit(function(evt){
		evt.preventDefault();
		loadFile();		
	});
	
	function loadFile() {
    	var input, file, fr;

	    if (typeof window.FileReader !== 'function') {
	      alert("The file API isn't supported on this browser yet.");
	      return;
	    }

	    input = document.getElementById('fileinput');
	    //input = $('#fileinput');
	    
	    if (!input) {

	      alert("Um, couldn't find the fileinput element.");
	    }
	    else if (!input.files) {
	    
	      alert("This browser doesn't seem to support the `files` property of file inputs.");
	    }
	    else if (!input.files[0]) {
	      alert("Please select a file before clicking 'Load'");
	    }
	    else {
			file = input.files[0];
			var ext = file.name.split('.').pop().toLowerCase();
			
			if($.inArray(ext, ['json']) == -1) {
			    alert('La cagaste!');
		    } else {
		    	var reader = new FileReader();
	        	reader.readAsText(file);
		        reader.onload = function(e) {
		            // browser completed reading file - display it
		            clear_data();
		            var data = JSON.parse(e.target.result);	            
		            attributes = data.attributes;
		            dependencies = data.dependencies;
		            load_data(dependencies);
		        };
		    }
	    }	    
  	}

  	function clear_data(){
  		$('#statemachine-demo').empty();
  	}

  	function load_data(dependencies){
  		var targets = {};
        var dependencies_str = '[';
  		for(var idx in dependencies) {
  			var data = dependencies[idx];
  			for (var key in data){
	        	var data_key = new Array(eval(key));
	        	var label = data_key.toString();
                var source_node = label.replace(/,/g, '');
	        	var source = {};
	        	var target = {};
	        	if (! targets[label]){	        		
	        		source = add_node(label);
	        		targets[label] = source;
	        	} else {
	        		source = targets[label];
	        	}
	        	var data_content = new Array(eval(data[key]));
                var label = data_content.toString();
                var end_node = label.replace(',', '');
	        	if (! targets[label]){
	        		target = add_node(label);
	        		targets[label] = target;
	        	} else {
	        		target = targets[label];
	        	}
	        	connections.push({source: source, target: target});
                // Update dependencies list
                dependencies_str += '{"' + source_node + '":"' + end_node + '"}, ';
	        }
		}
        // Update dependencies list field
        dependencies_str += ']'
        $('#id_dependencies_list').val(dependencies_str);
		load_connections();
  	}

  	function add_node(label){
  		var id_target = 'id_' + label;  		
  		var target = '<div class="w" id="' + id_target + '" style="left:' + Math.floor((Math.random() * 1000) + 1) + 'px; top:' + Math.floor((Math.random() * 500) + 1) + 'px;">' + label + '<div class="ep"></div></div>';
  		$('.statemachine-demo').append(target);
        return id_target;
  	}

  	function ini_library(){
  		// setup some defaults for jsPlumb.
	    instance = jsPlumb.getInstance({
	        Endpoint: ["Dot", {radius: 2}],
	        HoverPaintStyle: {strokeStyle: "#1e8151", lineWidth: 2 },
	        ConnectionOverlays: [
	            [ "Arrow", {
	                location: 1,
	                id: "arrow",
	                length: 14,
	                foldback: 0.8
	            } ],
	            [ "Label", { label: "FOO", id: "label", cssClass: "aLabel" }]
	        ],
	        Container: "statemachine-demo"
	    });

	    window.jsp = instance;

	    windows = jsPlumb.getSelector(".statemachine-demo .w");

	    // initialise draggable elements.
	    instance.draggable(windows);

	    // bind a click listener to each connection; the connection is deleted. you could of course
	    // just do this: jsPlumb.bind("click", jsPlumb.detach), but I wanted to make it clear what was
	    // happening.
	    instance.bind("click", function (c) {
	        instance.detach(c);
	    });

	    // bind a connection listener. note that the parameter passed to this function contains more than
	    // just the new connection - see the documentation for a full list of what is included in 'info'.
	    // this listener sets the connection's internal
	    // id as the label overlay's text.
	    instance.bind("connection", function (info) {
	        info.connection.getOverlay("label").setLabel(info.connection.id);
	    });

	    //instance = instance;
	    //windows = windows;

	    return {
	    	instance: instance,
	    	windows: windows
	    }
  	}

  	function load_connections(){
  		// setup some defaults for jsPlumb.

  		var var_init =  ini_library();
  		instance = var_init.instance;
  		windows = var_init.windows;

  		instance.batch(function () {
	        instance.makeSource(windows, {
	            filter: ".ep",
	            anchor: "Continuous",
	            connector: [ "StateMachine", { curviness: 20 } ],
	            connectorStyle: { strokeStyle: "#5c96bc", lineWidth: 2, outlineColor: "transparent", outlineWidth: 4 },
	            maxConnections: 1,
	            onMaxConnections: function (info, e) {
	                alert("Maximum connections (" + info.maxConnections + ") reached");
	            }
	        });

	        // initialise all '.w' elements as connection targets.
	        instance.makeTarget(windows, {
	            dropOptions: { hoverClass: "dragHover" },
	            anchor: "Continuous",
	            allowLoopback: true
	        });

	        // and finally, make a couple of connections	        
	        for (var idx in connections){
	        	instance.connect({ source: connections[idx].source, target: connections[idx].target});
	        }

	    });

	    jsPlumb.fire("jsPlumbDemoLoaded", instance);
  	}

  	$('.add_element').click(function(evt){
  		evt.preventDefault();

  		var label = prompt("Please enter your attr");
		if (label != null) {

            var id_target = add_node(label);
            var target = $('#' + id_target);

  		}
  	});


  	
  	$('#statemachine-demo').dblclick(function(e) {

  		var e0 = jsPlumb.addEndpoint("node0");

  		/*
  		var i = Math.floor((Math.random() * 1000) + 1);

  		var id_target = add_node(i);

  		var newState = $('#' + id_target);

	    newState.css({
	      'top': e.pageY,
	      'left': e.pageX
	    });
	    
	    var connect = $(newState).find('.ep');
	    
	    jsPlumb.makeTarget(newState, {
	      anchor: 'Continuous'
	    });
	    
	    jsPlumb.makeSource(connect, {
	      parent: newState,
	      anchor: 'Continuous'
	    });
		*/
    });


})