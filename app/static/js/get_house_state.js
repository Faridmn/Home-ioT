$(document).ready(() => {
  $('#house_state_button').click((e) => {
    e.preventDefault();
    const formData = {
      'uuid'    : $('#inspect_house_state_uuid').val(),
    };

    call_and_write_list('#inspect_house_state_form', formData);
  });
});
