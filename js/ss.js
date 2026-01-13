let arr = [55,6,1,4,8,0,12,77];
for(let i = 0; i < arr.length; i++) {
  for(let j = 0; j < arr.length; j++) {
    if(arr[j] > arr[j+1]) {
      let temp = arr[j];
      arr[j] = arr[j+1];
      arr[j+1] = temp;
    }
    console.log(arr);
    
  }
}
console.log(arr);