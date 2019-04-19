$(document).ready(() => {
  $('#device_state_button').click((e) => {
    e.preventDefault();
    const formData = {
      'uuid'    : $('#device_state_list').val(),
    };

    call_and_write_list('#device_state_form', formData);
  });
});
