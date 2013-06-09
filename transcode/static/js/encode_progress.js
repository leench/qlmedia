(function($) {

	$.fn.get_progress = function(options) {
		var defualts = { inv: 500 };
		var opts = $.extend({}, defualts, options);
		var obj = $(this);

		var pk = obj.attr("id").split("-")[1];

		var getres = function () {
			$.get('/get_encode_progress/?id=' + pk, function(data) {
				obj.text(data+'%');
				if ( data == "100.00" ) {
					window.clearInterval(timer);
					update_status(pk);
				}
			});
		};
		getres();
		timer = setInterval(getres, opts.inv);
	};

})(jQuery);