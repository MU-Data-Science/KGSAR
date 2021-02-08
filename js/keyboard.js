$(function(){
	var $write = $('#write'),
	shift = false,
	capslock = false;


	$('#keyboard li').click(function(){
		var $this = $(this),
		character = $this.html();

		// Shift keys
		if ($this.hasClass('left-shift') || $this.hasClass('right-shift')) {
			$('.letter').toggleClass('uppercase');
			$('.symbol span').toggle();

			shift = (shift === true) ? false : true;
			capslock = false;
			return false;
		}

		// Caps lock
		if ($this.hasClass('capslock')) {
			$('.letter').toggleClass('uppercase');
			capslock = true;
			return false;
		}

		// Delete
		if ($this.hasClass('delete')) {
			var html = $write.val();

			$write.val(html.substr(0, html.length - 1));
			return false;
		}

		// Special characters
		if ($this.hasClass('symbol')) character = $('span:visible', $this).html();
		if ($this.hasClass('space')) character = ' ';
		if ($this.hasClass('tab')) character = "\t";
		if ($this.hasClass('return')) character = "\n";

		// Uppercase letter
		if ($this.hasClass('uppercase')) character = character.toUpperCase();

		// Remove shift once a key is clicked
		// if (shift === true) {
		// 	$('.symbol span').toggle();
		// 	if (capslock === false) $('.letter').toggleClass('uppercase');
		//
		// 	shift = false;
		// }

		// Add the character
		$write.val($write.val() + character);
	});
});

function generate() {
	const doc = new docx.Document();
	var x = document.getElementById('write').value;

	doc.addSection({
		properties: {},
		children: [
			new docx.Paragraph({
				children: [
					new docx.TextRun({
						text: x,
						font: {
											name: "Nicolas De Valdivia Y Brizuela",
									},
					}),
				],
			}),
		],
	});

	docx.Packer.toBlob(doc).then(blob => {
		console.log(blob);
		saveAs(blob, "NewDocument.docx");
		console.log("Document created successfully");
	});
}
