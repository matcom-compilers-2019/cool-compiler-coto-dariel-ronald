   class Main {
    main() : Int {
            {
                let io: IO <- new IO in io.out_string("Hello World\n");
                let a:A <- new B, b: Int in
                                        let i:Int <- a.funk() + b, io: IO <- new IO in io.out_int(i);
                0;

            }
        };
    };
    class A {
       funk():Int {
            let x:Int in x + 1
       };
    };
    class B inherits A {
        funk():Int {
            42
        };
    };