.PHONY: all hello_c hello_jl hello_java clean

all: hello_c hello_java hello_jl

hello_c: hello.c
	gcc hello.c -o hello_c
	./hello_c

hello_jl: hello.jl
	julia hello.jl

hello_java: Hello.java
	javac Hello.java
	java Hello

clean:
	rm -f hello_c Hello.class
