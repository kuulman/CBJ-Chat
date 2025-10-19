const prompt = require('prompt-sync')({ sigint: true });
let Fnum = prompt('First Number: ');
let MOperator = prompt('Math Operator: ');
let Snum = prompt('Second Number: ');
Fnum = parseFloat(Fnum);
Snum = parseFloat(Snum);
const operators = {
  '+': (a, b) => a + b,
  '-': (a, b) => a - b,
  '*': (a, b) => a * b,
  '/': (a, b) => a / b,
  '%': (a, b) => a % b,
  '**': (a, b) => a ** b,
};

// Check if operator is valid
if (isNaN(Fnum) || isNaN(Snum)) {
    console.log('Please enter valid numbers for First Number and Second Number.');
}
if (operators[MOperator]) {
  const result = operators[MOperator](Fnum, Snum);
  console.log(`Result: ${Fnum} ${MOperator} ${Snum} = ${result}`);
} else {
  console.log('Invalid operator. Please use one of the following: +, -, *, /, %, **');
}