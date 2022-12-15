const $e = (elName, cl, parEl) => {
	if (elName == "svg" || elName == "path") {
		var e =  document.createElementNS("http://www.w3.org/2000/svg", elName);
		cl.forEach( val => e.setAttributeNS(null, val[0], val[1]));
	} else {
		var e = document.createElement (elName);
		cl.forEach( val => e.setAttribute(val[0], val[1]));
	}
	if (parEl) parEl.appendChild (e);
	return e;
}

function next_operator_number(){
	let button = document.getElementById('add-operator');
	let id = button.previousElementSibling.getElementsByTagName("input")[0].id;
	let pos = id.search('-');
	return id.substr(pos+1, id.length)*1+1;
}

function add_operator(){
    let button = document.getElementById('add-operator');
    let form = document.getElementById('repack-start');

	let div = $e("div", [], null);

	let next_operator_id = next_operator_number();

    let new_label = $e('label', [['for', 'id_operator-'+next_operator_id]], div);
	new_label.innerHTML = "Operátor "+next_operator_id;
    let new_input = $e('input', [['type', 'text'], ['id', 'id_operator-'+next_operator_id],
											['name', 'operator_'+next_operator_id], ['maxlength', '50'], ['required', '']], div);
    form.insertBefore(div, button);
}

function remove_last_operator(){
	let id = next_operator_number()-1;
	if(id===1){
		return;
	}
	let form = document.getElementById('repack-start');
	form.removeChild(document.getElementById('id_operator-'+id).parentElement);
}

function make_timer(){
	function time(){
		let time = document.getElementById('time');
		let t = 1*time.innerHTML;
		time.innerHTML = t+1+'';
	}

setInterval(time,1000);
}

function init_time(duration, start){
	let timeElement = document.getElementById('time');
	timeElement.innerHTML = duration +  Math.floor((Date.now()- Date.parse(start))/1000);
}