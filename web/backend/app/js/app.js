document.addEventListener('scroll', function () {
  expandTable("table")
}, { passive: true });


// toast
function showToast(header_info, body_info){
  toast = document.getElementById('toast');
  bsAlert = new bootstrap.Toast(toast);
  header = toast.getElementsByClassName("header")[0]
  header.innerHTML = header_info
  body = toast.getElementsByClassName("toast-body")[0]
  body.innerHTML = body_info
  bsAlert.show();
}