
'use strict';

var fileName = '';
var file = '';
$("#typetrain").click(function () {
  $("#typeContent").removeClass("hide");
});
$("#wholetrain").click(function () {
  $("#typeContent").addClass("hide");
});
$("#sli0").click(function () {
  $("#traingroup").removeClass("hide");
});
$("#sli1").click(function () {
  $("#traingroup").addClass("hide");
});
$("#sli2").click(function () {
  $("#traingroup").addClass("hide");
});
$('#loadfile').fileinput({
  showUpload: true,
  showRemove: false,
  showPreview: false,
  browseLabel: "浏览",
  removeLabel: "remove",
  uploadUrl: 'upload', // server upload action
  uploadLabel: "上传",
  maxFileCount: 1,
  uploadAsync: false,
});
$('#loadfile').on('filebatchpreupload', function (event, data, previewId, index) {
  console.log(data.files);
  fileName = $('#loadfile').text();
  console.log('File batch pre upload');
});

$('#loadfile').on('filebatchuploadsuccess', function (event, data, previewId, index) {
  file = data.files[0];
  console.log(file);
  console.log('File batch upload success');
});
$('#calc').click(function () {
  $(this).attr("disabled", "true");
  $("#jindu").show();
  $.ajax({
    url: '/classify',
    type: 'GET',
    data: {},
    async: true,
    dataType: 'text',
    success: function (data) {
      $("#jindu").hide();
      showResult(data);
      console.log(data);
      console.log('分类成功');
    }
  })
})
function showResult(data) {
  var result = data.split(',')
  switch(result[0]){
    case "正常":
      $('.legaltxt').removeClass('hide');
      $('.illegaltxt').addClass('hide');
      break;
    case "不正常":
      $('.illegaltxt').removeClass('hide');
      $('.legaltxt').addClass('hide');
      break;
    default:
      $('.legaltxt').removeClass('hide');
      $('.illegaltxt').addClass('hide');
  }
  $('.result').html(result[1]);
}