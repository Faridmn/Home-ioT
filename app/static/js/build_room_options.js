function build_room_options() {
  $.getJSON(
    '/get-room',
    data => {
      $('.room_list').find('option').remove();

      $.each(data, (key, val) => {
        const option_item = '<option value="' + val['name'] + '">' + val['name'] + '</option>';
        $('.room_list').append(option_item);
      });
    }
  );
}

function build_optional_room_options() {
  $.getJSON(
    '/get-room',
    data => {
      $('.optional_room_list').find('option').remove();

      const all_option = '<option value="">All Rooms</option>';
      $('.optional_room_list').append(all_option);

      $.each(data, (key, val) => {
        const option_item = '<option value="' + val['name'] + '">' + val['name'] + '</option>';
        $('.optional_room_list').append(option_item);
      });
    }
  );
}

$(document).ready(build_room_options());
$(document).ready(build_optional_room_options());

