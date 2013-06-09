var encode_status = {
	'0': '无状态',
	'1': '列队',
	'2': '转码中',
	'3': '转码完成',
	'4': '转码失败'
}

var update_status = function(pk) {
	$.getJSON('/get_status/?id=' + pk, function(data) {
		if ( data.es == 2 ) {
			var html = '<span class="encoding_progress" id="pk-' + pk + '"></span>';
			$("span#es-" + pk).html(html);
			$("#pk-" + pk).get_progress({});
		} else {
			$("span#es-" + pk).text(encode_status[data.es]);
		}
		$("span#ts-" + pk).text(data.ts);
		$("span#ps-" + pk).text(data.ps);
	});
};

$(document).ready(function () {

	var get_status = function() {
		$("tbody tr").each(function( index ) {
			var obj = $(this);
			var pk = obj.find('input.action-select').val();
			update_status(pk);
		});
	};
	get_status();
});