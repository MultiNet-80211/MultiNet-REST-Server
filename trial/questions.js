
	//current screen
	var screen = 0;
	
	var start = function() {
		//$.Storage.set("screen1","1,2,3,4,5,6,7,8,9");
		alert($.Storage.get("screen1"));
		alert($.Storage.get("screen2"));
		screen = getScreen();
	};
	
	var save = function() {
	   
	   var data = [];
	   
	   data.push(getPid());
	   
	   $(".answer").each(function(i) {
	   		var store = '';
	   		$("input,select,textarea",this).each(function(j) {
	   			
	   			switch(this.type) {
	   			  case "text":
	   			    store = this.value;
	   			  break;
	   			  case "radio":
	   			    if(this.checked) {
	   				  store = this.value;
	   			    }
	   			  break;
	   			  case "checkbox":
	   			    if(this.checked) {
	   			  	  store = this.value;
	   			    }
	   			  break;
	   			  case "select-one":
	   			  	store = this.value;
	   			  break;
	   			  case "textarea":
	   			  	store = this.value;
	   			  break;
	   			}
	   		});
	   		
	   		data.push(store)
	   });
	   
	   $.Storage.set("screen" + screen,data.toString());
	   
	   //save the screen
	   
	   
	   screen = getScreen(screen + 1);
	};
	
	var getScreen = function (screenNo) {
		if(screenNo == null) {
			screenNo = 1;
		}
		url = "./screens/screen" + screenNo + ".html";
		$("#form").load(url);
		
		$('html, body').animate({scrollTop:0}, 'slow');
		
		return screenNo;
	};
	
	pid = "";
	var getPid = function() {
	  if(pid == "") {
	  	pid = new Date().getTime();
	  }
	  return pid;
	}
	
	
