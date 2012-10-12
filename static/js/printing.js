var printing = printing||{};

printing.serviceURL = '/LabBook/render/print_pdf';

printing.print_page = function() {
	var current_path = window.location.toString();
	maths = $('script[type^="math/tex"]');
	maths_arr = [];
	for (i=0; i< maths.length; i++) {
		var temp = $('<div></div>').append($(maths[i]).prev().clone());
		maths_arr.push(temp.html());
	}
	var styles = $('style')
	var mj_css = styles[styles.length - 1].textContent;
	var data = {};
	data.maths = maths_arr;
	data.mj_css = mj_css;
	data.current_path = current_path;
	$.post(printing.serviceURL, data, function (data) {
		var printjob_id = data['printid'];
		var job_complete = false;
		(function poll() {
		    setTimeout(function () {
		    	console.log('Print job pending...');
		        $.ajax({
		            type: 'GET',
		            dataType: 'json',
		            url: printing.serviceURL + '/' + printjob_id,
		            success: function (data, textStatus, xhr) {
						if (xhr.status != 202) {
							if (xhr.status == 201) {
								console.log('Job complete, fetching...');
								if ($('#print_spooler').length == 0) {
									$(document.body).append('<iframe style="display: none" id="print_spooler"></iframe>');
								}
								$('#print_spooler').attr('src', printing.serviceURL + '/' + printjob_id + '/fetch');
							} else {
								console.log('Error: ' + xhr.status);
							}
							job_complete = true;
						}
         					},
         					error: function(xhr, textStatus, error) {
         						console.log('Error: ' + xhr.status + ' ' + error);
         						job_complete = true;
         					},
		            complete: function() { if (!job_complete) { poll(); } }
     					});
 					}, 2500);
		})();
	}, 'json');
};