(function($) {

	$.fn.get_transfer_progress = function(options) {
		var defualts = { inv: 1000 };
		var opts = $.extend({}, defualts, options);
		var obj = $(this);

		var pk = obj.attr("id").split("-")[1];

		var getres = function () {
			$.get('/get_transfer_progress/?id=' + pk, function(data) {
				obj.text(data+'%');
				if ( data == "100" ) {
					eval("window.clearInterval(timer_transfer_" + pk + ")");
					//window.clearInterval(timer);
					//setTimeout(update_status(pk), 1000);
				}
			});
		};
		getres();
		eval("timer_transfer_" + pk + " = setInterval(getres, opts.inv)");
		//timer = setInterval(getres, opts.inv);
	};

})(jQuery);