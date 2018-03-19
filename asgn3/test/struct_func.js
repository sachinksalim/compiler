function f (x)
{
  x.a = 'a';
  x.b = 47114711;
  x.c = 'c';
  x.d = 1234;
  x.e = 3.141592897932;
  x.f = '*';
  x.name = "abc";
}

function main (){
    var k = {};
    f(k);
    return 0;
}
main();
