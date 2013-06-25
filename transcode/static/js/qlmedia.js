$(document).ready(function () {
	$('#id_file').fineUploader({
		request: {
			endpoint: '/ajax_upload/'
		},
		multiple: false,
		validation: {
			allowedExtensions: ['avi', 'flv', 'mp4', 'f4v', 'mkv'],
			// sizeLimit: 51200 // 50 kB = 50 * 1024 bytes
		},
		text: {
			uploadButton: 'Click or Drop'
		},
		showMessage: function(message) {
			// Using Bootstrap's classes
			$('#restricted-fine-uploader').append('<div class="alert alert-error">123' + message + '</div>');
		}
	}).on('complete', function(event, id, fileName, responseJSON) {
		console.info(responseJSON);
		if (responseJSON.success) {
			//$(this).append('<input id="id_file" name="file" value="' + responseJSON.filename + '" />');
			$('input#id_file').val(responseJSON.filename);
		}
	});
});