$(document).ready(() => {
  $('#add_device_button').click((e) => {
    e.preventDefault();
    const formData = {
      'name'        : $('#add_device_name').val(),
      'location'    : $('#add_device_location').val(),
      'device_type' : $('#add_device_type').val()
    };

    call_and_write_text('#add_device_form', formData);
  });
});
