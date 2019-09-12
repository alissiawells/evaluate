/*!
 * IE10 viewport hack for Surface/desktop Windows 8 bug
 * Copyright 2014-2015 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 */

// See the Getting Started docs for more information:
// http://getbootstrap.com/getting-started/#support-ie10-width

$(document).ready(function(){
$('#is_rejected').change(function(){
if(this.checked)
{
  $('#hidable').fadeOut('fast');
  var x = document.getElementById('id_text_answer');
  $(x).prop('required', false);
  // document.getElementById('id_text_answer').prop('required', !checked)
  // document.getElementById('id_text_answer').setAttribute('required','required');
}
else
{
  $('#hidable').fadeIn('fast');
  var ta = document.getElementById("textAnswer").value;
  if (ta=="True")
  {
    var x = document.getElementById('id_text_answer');
    $(x).prop('required', true);
  }
  // document.getElementById('id_text_answer').removeAttribute('required');
  // $('#id_text_answer').removeAttr('required');
}
});
});
