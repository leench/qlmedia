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
	} catch (err) {
	}
	try {
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
			$("span#es-" + pk).html('<img alt="True" src="/static/admin/img/icon-yes.gif"> '+encode_status[data.es]);
		} else {
			$("span#es-" + pk).html(encode_status[data.es]);
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
			$("span#ts-" + pk).html('<img alt="True" src="/static/admin/img/icon-yes.gif"> '+transfer_status[data.ts]);
		} else {
			$("span#ts-" + pk).html(transfer_status[data.ts]);
		}

		// publish
		if ( data.ps == true ) {
			$("span#ps-" + pk).html('<img alt="True" src="/static/admin/img/icon-yes.gif"> 已发布');
		} else {
			$("span#ps-" + pk).html('<img alt="False" src="/static/admin/img/icon-no.gif"> 未发布');
		}
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