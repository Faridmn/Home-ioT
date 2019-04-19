$(document).ready(() => {
  $('#list_device_events_button').click((e) => {
    e.preventDefault();
    const formData = {
      'uuid'    : $('#list_device_events_list').val(),
      'from_ts' : encodeURI($('#list_device_events_from').val()),
      'to_ts'   : encodeURI($('#list_device_events_to').val())
    };

    call_and_write_list('#list_device_events_form', formData);
  });
});
