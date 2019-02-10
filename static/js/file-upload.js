// FILE UPLOAD

// triggered on image selection
function readURL(input) {
    if (input.files && input.files[0]) {

        let reader = new FileReader();

        reader.onload = function (e) {

            $('.file-upload-image').attr('src', e.target.result);
            $('.image-title').html(input.files[0].name);

            $('.file-upload-content').show();
            $('.image-upload-wrap').hide();
        };

        reader.readAsDataURL(input.files[0]);

    } else {
        removeUpload();
    }
}

// triggered on clicking the Remove button
function removeUpload() {
    let fileUploadInput = $('.file-upload-input');
    fileUploadInput.replaceWith(fileUploadInput.val('').clone(true));
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
}

(function attachFileUploadDragAndDropEvents(){
    let imageUploadWrap = $('.image-upload-wrap');
    imageUploadWrap.bind('dragover', function () {
        $('.image-upload-wrap').addClass('image-dropping');
    });
    imageUploadWrap.bind('dragleave', function () {
        $('.image-upload-wrap').removeClass('image-dropping');
    });
})();
