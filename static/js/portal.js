
document.addEventListener('DOMContentLoaded', function () {
    var copyInput = document.getElementById('copyInput');

    copyInput.addEventListener('click', function () {
        // Select the text in the input field
        copyInput.select();
        copyInput.setSelectionRange(0, 99999); // For mobile devices

        // Copy the selected text to the clipboard
        document.execCommand('copy');

        // Deselect the text to avoid visual confusion
        copyInput.setSelectionRange(0, 0);

        // You can optionally provide user feedback, e.g., show a tooltip or a message
        alert('Text copied to clipboard: ' + copyInput.value);
    });
});


// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();
