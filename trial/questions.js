
	//current screen
	var screen = 0;
	var userID = '';
	var clock = new Date();
	
	var setDate = function (id) {
		$('#'+id).val(new Date().getTime());
	}
	
	var start = function() {
		//$.Storage.set("screen1","1,2,3,4,5,6,7,8,9");
<<<<<<< HEAD
		alert($.Storage.get("screen1"));
		alert($.Storage.get("screen2"));
=======
		//alert($.Storage.get("screen1"));
		
		userID = clock.getTime();
		
>>>>>>> branch 'master' of ssh://git@github.com/Toshbrown/Multinet-REST-Server.git
		screen = getScreen();
		
	};
	
	var save = function() {
	   
	   var data = [];
<<<<<<< HEAD
	   
	   data.push(getPid());
	   
=======
	   data.push(userID);
>>>>>>> branch 'master' of ssh://git@github.com/Toshbrown/Multinet-REST-Server.git
	   $(".answer").each(function(i) {
	   		var store = '';
	   		$("input,select,textarea",this).each(function(j) {
<<<<<<< HEAD
	   			
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
=======
	   			if(this.type != 'radio' &&  this.type != 'checkbox') {
	   				store = this.value;
	   			} else if (this.checked) {
	   				store = this.value;
>>>>>>> branch 'master' of ssh://git@github.com/Toshbrown/Multinet-REST-Server.git
	   			}
	   		});
	   		
	   		data.push(store);
	   });
<<<<<<< HEAD
	   
	   $.Storage.set("screen" + screen,data.toString());
	   
	   //save the screen
	   
=======
	   $('#form').removeData("screen" + screen);
	   $('#form').data("screen" + screen, data.toString());
>>>>>>> branch 'master' of ssh://git@github.com/Toshbrown/Multinet-REST-Server.git
	   
	   screen = getScreen(screen + 1);
	   
	};
	
	var saveALL = function () {
		if($("#saveALL").html() == 1) {
			$("#form").load('/saveAll/',$('#form').data(),function(){
				userID = '';
			});
		}
	};
	
	var getScreen = function (screenNo) {
		if(screenNo == null) {
			screenNo = 1;
		}
		url = "./screens/screen" + screenNo + ".html";
		
		$("#form").load(url,saveALL);
		
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
	
	
	
	
