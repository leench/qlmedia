var encode_status = {
	'0': '无状态',
	'1': '列队',
	'2': '转码中',
	'3': '转码完成',
	'4': '转码失败'
}

var transfer_status = {
	'0': '无状态',
	'1': '列队',
	'2': '上传中',
	'3': '上传完成',
	'4': '上传失败'
}

var update_status = function(pk) {
	try {
		eval("window.clearInterval(timer_encode_" + pk + ")");
		eval("window.clearInterval(timer_transfer_" + pk + ")");
	} catch (err) {
	}
	$.getJSON('/get_status/?id=' + pk, function(data) {
		// encode
		if ( data.es == 2 ) {
			var ehtml = '<span class="encoding_progress" id="epk-' + pk + '"></span>';
			$("span#es-" + pk).html(ehtml);
			$("#epk-" + pk).get_encode_progress({});
		} else if ( data.es == 3 ) {
			try {
				eval("window.clearInterval(timer_encode_" + pk + ")");
			} catch (err) {
			}
			$("span#es-" + pk).text(encode_status[data.es]);
		} else {
			$("span#es-" + pk).text(encode_status[data.es]);
		}

		// transfer
		if ( data.ts == 2 ) {
			var thtml = '<span class="transferring_progress" id="tpk-' + pk + '"></span>';
			$("span#ts-" + pk).html(thtml);
			$("#tpk-" + pk).get_transfer_progress({});
		} else if ( data.ts == 3 ) {
			try {
				eval("window.clearInterval(timer_transfer_" + pk + ")");
			} catch (err) {
			}
			$("span#ts-" + pk).text(transfer_status[data.ts]);
		} else {
			$("span#ts-" + pk).text(transfer_status[data.ts]);
		}

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
	setInterval(get_status, 3000);
});