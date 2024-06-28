let myModal;

function switchPage(e) {
  fetch(e.dataset.url)
    .then((response) => response.text())
    .then((data) => document.querySelector('#page_data').innerHTML = data)
}

function loadTable(table_id) {
  let table = document.querySelector("#" + table_id)
  fetch(table.dataset.url)
    .then((response) => response.json())
    .then((data) => fillTable(table, data))
}

function fillTable(table, data) {
  let body = table.querySelector('tbody')
  let ths = table.querySelectorAll('th')
  let row_id = table.dataset.rowid
  let tds = getTds(ths)
  body.innerHTML = ''
  for (let i = 0; i < data.length; i++) {
    let row = body.insertRow()
    if (i > 20) {
      row.setAttribute("style", "display:none")
    } else {
      row.setAttribute("style", "display:")
    }
    row.id = data[i][row_id]
    row.dataset.found = true
    addRow(row, data[i], tds)
  }
  table.closest(".table-responsive").querySelector('#table_count').textContent = data.length
}

function getTds(ths) {
  let tds = []
  for (let i = 1; i < ths.length - 1; i++) {
    tds.push(ths[i].dataset.name)
  }
  return tds
}

function addRow(row, data, tds) {
  row.innerHTML = `<td>
  <span class="circle ${data.color} sx"></span>
  </td>`
  for (const td of tds) {
    row.innerHTML += `<td onclick="showEditModal(this)">` + data[td] + `</td>`
  }
  row.innerHTML += `<td>
    <input 
      class="form-check-input bg-secondary-subtle"
      type="checkbox"
      onclick="checkRow(this)">
  </td>`

}

function expandTable(table_id) {
  if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
    let table = document.querySelector("#" + table_id)
    let trs = table.querySelectorAll("tr")
    for (let i = 1, j = 0; i < trs.length && j < 20; i++) {
      if ((trs[i].dataset.found = true) && (trs[i].style.display)) {
        trs[i].style.display = ""
        j++
      }
    }
  }
}

function checkRow(e) {
  let table = e.closest(".table-responsive")
  let panel_one = table.querySelector('#panel_one')
  let panel_two = table.querySelector('#panel_two')
  let checked_count = table.querySelector('#checked_count')
  let check_allrow = table.querySelector('#check_allrow')
  panel_one.classList.add('d-none')
  panel_two.classList.remove('d-none')
  count = checked_count.textContent
  if (e.checked) {
    count++
  } else {
    count--
  }
  if (count == 0) {
    check_allrow.checked = false
    panel_two.classList.add('d-none')
    panel_one.classList.remove('d-none')
  }
  checked_count.textContent = count
}

function checkAllRow(e) {
  let table = e.closest(".table-responsive")
  let panel_one = table.querySelector('#panel_one')
  let panel_two = table.querySelector('#panel_two')
  let checked_count = table.querySelector('#checked_count')
  let trs = table.querySelectorAll("tr")
  panel_one.classList.add('d-none')
  panel_two.classList.remove('d-none')
  count = 0
  for (i = 1; i < trs.length; i++) {
    if (trs[i].style.display != "none") {
      if (e.checked) {
        trs[i].querySelector('input').checked = true
        count++
      } else {
        trs[i].querySelector('input').checked = false
        count == 0
      }
    }
  }
  if (count == 0) {
    panel_two.classList.add('d-none')
    panel_one.classList.remove('d-none')
  }
  checked_count.textContent = count
}


function deleteRow(e) {
  let table = e.closest(".table-responsive")
  let tbody = table.querySelector("tbody")
  let trs = tbody.querySelectorAll("tr")
  let url = table.dataset.url
  trs.forEach(tr => {
    if (tr.querySelector("input").checked == true) {
      fetch(url + '/' + tr.id, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
      })
        .then((response) => tr.remove())
        .then(showToast("Success", "Deleted"))
        .catch((error) => {
          showToast("Error", "Not deleted")
          console.error('Error:', error);
        });
    }
  })
  switchPanel(table)
}

function copyRow(e) {
  let table = e.closest(".table-responsive")
  let tbody = table.querySelector("tbody")
  let trs = tbody.querySelectorAll("tr")
  let url = table.dataset.url
  trs.forEach(tr => {
    let check_box = tr.querySelector("input")
    if (check_box.checked == true) {
      check_box.checked = false;
      fetch(url + tr.id + "/copy")
        .then((response) => response.json())
        .then((data) => updateRow(table, data))
        .then(showToast("Success", "Copied"))
        .catch((error) => {
          showToast("Error", "Not copied")
          console.error('Error:', error);
        });
    }
  })
  switchPanel(table)
}

function updateRow(table, data) {
  let body = table.querySelector('tbody')
  let ths = table.querySelectorAll('th')
  let tr_id = "[id='" + data[table.dataset.rowid] + "']"
  let tds = getTds(ths)
  let row = table.querySelector(tr_id)
  if (!row) {
    row = body.insertRow()
    row.id = data[table.dataset.rowid]
  }
  addRow(row, data, tds)
}

function makeThead(tds) {
  let thead = `
    <th></th>
  `
  for (const [key, value] of Object.entries(tds)) {
    thead += `
      <th
        data-name="${key}"
        onclick="sortTableByColumn(this)">
        ${value}
      </th>`
  }
  thead += `
    <th>
      <input 
        class="form-check-input bg-secondary-subtle" 
        type="checkbox" 
        onclick="checkAllRow(this)"
        id="check_allrow">
    </th>`
  return thead
}

// modal
function showEditModal(e) {
  let table = e.closest(".table-responsive")
  let url = table.dataset.url + '/' + e.closest('tr').id
  let modal = document.querySelector('.modal')
  myModal = new bootstrap.Modal(modal)
  let modal_body = modal.querySelector('.modal-body')
  let modal_status = modal.querySelector('.modal-status')
  let modal_edit = modal.dataset.modal_edit
  modal_status.innerHTML = ''
  let general_inputs = modal_body.querySelector('#general_inputs').querySelectorAll('input')
  let row_inputs = modal_body.querySelector('#row_inputs')
  let row_inputs_name = modal_body.querySelector('#row_inputs_name')
  row_inputs.innerHTML = ''
  let row0 = modal_body.querySelector('#row-0')
  let btn = modal.querySelector('.btn-save')
  myModal.show()
  fetch(url)
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      if (data.status) {
        let status_div = document.createElement('div');
        status_div.innerHTML = data.status;
        modal_status.appendChild(status_div);
      }
      if (data.color) {
        let color_div = document.createElement('div');
        color_div.innerHTML = `<span class="circle ${data.color}"></span>`;
        modal_status.appendChild(color_div);
      }
      for (input of general_inputs) {
        input.value = data[input.id]
      }
      if (row_inputs.dataset.rows_name) {
        for (const row of data[row_inputs.dataset.rows_name]) {
          if (modal_edit == "true") {
            let newRow = row0.cloneNode(true);
            let row0_inputs = newRow.querySelectorAll('input')
            for (input of row0_inputs) {
              for (field in row[input.id]) {
                input.value = row[input.id]
              }
            }
            newRow.classList.remove('d-none')
            row_inputs.appendChild(newRow);
          } else {
            let rows = `<div class="pt-3 row" id="row-1">`
            for (const [key, value] of Object.entries(row)) {
              row_inputs_name.classList.remove('d-none')
              rows += `
              <div class="mb-3 row justify-content-center">
                <label 
                  for="${key}" 
                  class="col-sm-2">
                  ${key}
                </label>
                <div class="col-sm-7">
                  <input 
                    type="text" 
                    class="form-control" 
                    id="${key}" 
                    placeholder="${value}"
                    value="${value}">
                </div>
              </div>`
            }
            rows += '</div'
            row_inputs.innerHTML = rows;
          }
        }
      }
      btn.dataset.url = url
      btn.dataset.method = 'PUT'
    })
}

function showAddModal(e) {
  let table = e.closest(".table-responsive")
  let url = table.dataset.url
  let modal = document.querySelector('.modal')
  myModal = new bootstrap.Modal(modal)
  let modal_body = modal.querySelector('.modal-body')
  let inputs = modal_body.querySelectorAll('input')
  let row_inputs = modal_body.querySelector('#row_inputs')
  row_inputs.innerHTML = ''
  let btn = modal.querySelector('.btn-save')
  btn.dataset.url = url
  btn.dataset.method = 'POST'
  for (input of inputs) {
    input.value = ''
  }
  myModal.show()
}


function saveModal(e) {
  let table = document.querySelector(".table-responsive")
  let modal = document.querySelector('.modal')
  myModal.hide()
  let modal_body = modal.querySelector('.modal-body')
  let general_inputs = modal_body.querySelector('#general_inputs').querySelectorAll('input')
  let row_inputs = modal_body.querySelector('#row_inputs')
  let div_inputs = row_inputs.querySelectorAll('.row')
  let rows_name = row_inputs.dataset.rows_name
  let data = {}
  data[rows_name] = []
  for (input of general_inputs) {
    data[input.id] = input.value
  }
  for (row of div_inputs) {
    let inputs = row.querySelectorAll('input')
    let input_pair = {}
    for (input of inputs) {
      input_pair[input.id] = input.value;
    }
    data[rows_name].push(input_pair)
  }
  fetch(e.dataset.url, {
    method: e.dataset.method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      updateRow(table, data)
    })
    .then(showToast("Success", "Saved"))
    .catch((error) => {
      showToast("Error", "Not saved")
      console.error('Error:', error);
    });

}

function addModalRow(button) {
  const existingRow = document.getElementById('row-0');
  const newRow = existingRow.cloneNode(true);
  newRow.classList.remove('d-none')
  const rowInputs = document.getElementById('row_inputs');
  rowInputs.appendChild(newRow);
}

function delModalRow(button) {
  button.closest("div").remove()
}

//panel
function switchPanel(table) {
  table.querySelector('#panel_one').classList.remove('d-none')
  table.querySelector('#panel_two').classList.add('d-none')
  table.querySelector('#check_allrow').checked = false;
  table.querySelector('#checked_count').textContent = 0;
}


async function exportData(e) {
  let table = e.closest(".table-responsive")
  let url = table.dataset.url
  const dataToExport = await fetch(url)
  .then((response) => response.json())
  try {
    const jsonData = JSON.stringify(dataToExport, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'exported_data.json';
    a.click();
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error exporting data:', error);
  }
}

function importData(e) {
  let table = e.closest(".table-responsive")
  let url = table.dataset.url + "/import"
  const selectedFile = e.files[0];

  if (selectedFile) {
    const reader = new FileReader();

    reader.onload = function(event) {
      const fileContent = event.target.result;

      try {
        const parsedData = JSON.parse(fileContent);
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(parsedData),
        })
        .then((response) => {
          return response.json()
        })
        .then((data) => {
          fillTable(table, data)
        })
        .then(showToast("Success", "Imported"))
        .catch((error) => {
          showToast("Error", "Not imported")
          console.error('Error:', error);
        });
      } catch (error) {
        console.error('Error importing data:', error);
      }
    };

    reader.readAsText(selectedFile);
  }
}

function searchRow(searchText) {
    console.log(searchText)
    let table = document.querySelector('.table-responsive');
    let rows = table.querySelectorAll('tbody tr');

    rows.forEach(row => {
        let cells = row.querySelectorAll('td');
        let found = false;
        cells.forEach(cell => {
            if (cell.textContent.toLowerCase().includes(searchText.toLowerCase())) {
                found = true;
            }
        });
        if (found) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

