function main(n: number) {
  var c: number = probability(n);
  console.log(23);
}

function probability(n: number): number {
  var prob: number = 1;

  for (let i = 1; i < n; i = i + 1) {
    var log: number = 365 - i
    var logUpdated: number = log / 365
    prob = prob * logUpdated
  }
  return 1 - prob * 100 / 100;
}