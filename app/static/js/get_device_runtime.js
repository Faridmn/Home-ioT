$(document).ready(() => {
  $('#list_device_runtime_button').click((e) => {
    e.preventDefault();
    const formData = {
      'uuid'    : $('#list_device_runtime_list').val(),
      'from_ts' : encodeURI($('#list_device_runtime_from').val()),
      'to_ts'   : encodeURI($('#list_device_runtime_to').val())
    };

    call_and_write_json('#list_device_runtime_form', formData);
  });
});
