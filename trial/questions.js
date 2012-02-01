
	//current screen
	var screen = 0;
	var userID = '';
	var clock = new Date();
	
	var setDate = function (id) {
		$('#'+id).val(new Date().getTime());
	}
	
	var start = function() {
		//$.Storage.set("screen1","1,2,3,4,5,6,7,8,9");
		//alert($.Storage.get("screen1"));
		
		userID = clock.getTime();
		
		screen = getScreen();
		
	};
	
	var save = function() {
	   
	   var data = [];
	   data.push(userID);
	   $(".answer").each(function(i) {
	   		var store = '';
	   		$("input,select,textarea",this).each(function(j) {
	   			if(this.type != 'radio' &&  this.type != 'checkbox') {
	   				store = this.value;
	   			} else if (this.checked) {
	   				store = this.value;
	   			}
	   		});
	   		
	   		data.push(store);
	   });
	   $('#form').removeData("screen" + screen);
	   $('#form').data("screen" + screen, data.toString());
	   
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
	
	
	
	
	
