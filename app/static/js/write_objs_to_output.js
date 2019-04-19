function write_list_to_output(list) {
  const items = JSON.parse(list);
  $('#output').empty();
  $('#output').append('<ul class="list-group"></ul>');
  for (i in items) {
    const item_text = JSON.stringify(items[i]);
    $('#output ul').append($('<li class="list-group-item">')
                            .text(item_text)
                          );
  }
  $('#output').show()
}

function write_json_to_output(obj) {
  const items = JSON.parse(obj);
  $('#output').empty();
  $('#output').append('<ul class="list-group"></ul>');
  for (key in items) {
    const item_text = JSON.stringify(items[key]);
    $('#output ul').append($('<li class="list-group-item">')
                            .text(key + ": " + item_text)
                          );
  }
  $('#output').show()
}

function call_and_write_text(formId, formData) {
    $.ajax({
      url     : $(formId).attr('action'),
      data    : formData,
      success : (result) => { $('#output').html(result); $('#output').show() },
      always  : () => { $(formId).submit(); },
      error   : (xhr, status, error) => { alert(error); }
    });
}

function call_and_write_list(formId, formData) {
    $.ajax({
      url     : $(formId).attr('action'),
      data    : formData,
      success : (result) => { write_list_to_output(result); },
      always  : () => { $(formId).submit(); },
      error   : (xhr, status, error) => { alert(error); }
    });
}

function call_and_write_json(formId, formData) {
    $.ajax({
      url     : $(formId).attr('action'),
      data    : formData,
      success : (result) => { write_json_to_output(result); },
      always  : () => { $(formId).submit(); },
      error   : (xhr, status, error) => { alert(error); }
    });
}
