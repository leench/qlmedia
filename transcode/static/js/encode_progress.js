(function($) {

	$.fn.get_encode_progress = function(options) {
		var defualts = { inv: 1000 };
		var opts = $.extend({}, defualts, options);
		var obj = $(this);

		var pk = obj.attr("id").split("-")[1];

		var getres = function () {
			$.get('/get_encode_progress/?id=' + pk, function(data) {
				obj.text(data+'%');
				if ( data == "100.00" ) {
					eval("window.clearInterval(timer_encode_" + pk + ")");
					//window.clearInterval(timer);
					//setTimeout(update_status(pk), 1000);
//					setTimeout(function() {
//
//					}, 1000);
//					update_status(pk);
				}
			});
		};
		getres();
		eval("timer_encode_" + pk + " = setInterval(getres, opts.inv)");
		//timer = setInterval(getres, opts.inv);
	};

})(jQuery);