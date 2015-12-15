
'use strict';

var fileName = '';
var file = '';
var uploadComplete = false;
var pageTag = 0;
$('#calc').attr("disabled", "true");
$('#title').html('请上传文本文件');
$('#contentGroup').hide();
$("#typetrain").click(function () {
  $("#typeContent").removeClass("hide");
});
$("#wholetrain").click(function () {
  $("#typeContent").addClass("hide");
});
$("#sli0").click(function () {
  $('#title').html('请上传文本文件');
  $('#calc').attr("disabled", "true");
  $('#contentGroup').hide();
  $("#traingroup").removeClass("hide");
  pageTag = 0;
});
$("#sli1").click(function () {
  $('#title').html('请上传文本文件,以应属类别命名该文件');
  $('#calc').removeAttr("disabled");
  $('#contentGroup').hide();
  $('#resultContent').hide();
  $("#traingroup").addClass("hide");
  pageTag = 1;
});
$("#sli2").click(function () {
  $('#title').html('请上传文本文件或将文本内容复制到文本框');
  $('#contentGroup').show();
  $('#applyResult').hide();
  $('#calc').removeAttr("disabled");
  $("#traingroup").addClass("hide");
  pageTag = 2;
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
  //allowedFileExtensions:['txt']
});
$('#loadfile').on('filebatchpreupload', function (event, data, previewId, index) {
  console.log(data.files);
  fileName = data.files[0].name;
  console.log(fileName);
  uploadComplete = false;
});

$('#loadfile').on('filebatchuploadsuccess', function (event, data, previewId, index) {
  file = data.files[0];
  console.log(file);
  uploadComplete = true;
  console.log('File batch upload success');
});
$('#calc').click(function () {

  if (uploadComplete) {
    $('#resultContent').hide();
    $('#applyResult').hide();
    $("#jindu").show();
    $.ajax({
      url: '/classify1',
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
  }
  else if ($('#textContent').val() != '') {
    var content = new Object();
    $('#applyResult').hide();
    content.data = $('#textContent').val();
    $("#jindu").show();
    $.ajax({
      url: '/classify2',
      type: 'POST',
      data: content,
      async: true,
      dataType: 'text',
      success: function (data) {
        $("#jindu").hide();
        showResult(data);
        console.log(data);
        console.log('分类成功');
      }
    })
  } else {
    alert('请上传文件或复制内容到文本框');
  }

})
function showResult(data) {
  var result = data.split(',');
  if (pageTag == 1) {
    switch (result[0]) {
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
    $('.expect').html(fileName.split('.')[0]);
    $('#resultContent').show();
    uploadComplete = false;  
  } else if (pageTag == 2) {
    $('.result').html(result[1]);
    $('.expect').html(result[0]);
    uploadComplete = false;
    $('#applyLabel').html('分类结果为'+result[1]+',请进行人工研判！');
    $('#applyResult').show();
    $('#textContent').val('');
  }

}