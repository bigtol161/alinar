document.addEventListener('DOMContentLoaded', function () {
  function maskPhone(input) {
    input.setAttribute('autocomplete', 'tel');
    input.addEventListener('input', function () {
      var d = input.value.replace(/\D/g, '');
      if (d.charAt(0) === '8') d = '7' + d.slice(1);
      if (d.charAt(0) === '9') d = '7' + d;
      if (d.charAt(0) !== '7') d = '7' + d;
      d = d.slice(0, 11);
      var out = '+7';
      if (d.length > 1) out += ' (' + d.slice(1, 4);
      if (d.length >= 4) out += ') ' + d.slice(4, 7);
      if (d.length >= 7) out += '-' + d.slice(7, 9);
      if (d.length >= 9) out += '-' + d.slice(9, 11);
      input.value = out;
    });
  }
  document.querySelectorAll('input[name="phone"]').forEach(maskPhone);
});
