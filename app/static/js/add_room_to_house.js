$(document).ready(() => {
  $('#add_room_to_house_button').click((e) => {
    e.preventDefault();
    const formData = {
      'room' : $('#add_room_to_house_name').val(),
      'uuid' : $('#add_room_to_house_uuid').val(),
    };

    call_and_write_text('#add_room_to_house_form', formData);
  });
});
