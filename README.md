# Socket Ring

Ring Network to learn about sockets (2016)

to learn more about sockets, I'm making a ring network
just for fun. This will be a collection of 
scripts/apps that have an input socket and an output socket. They
are connected in a ring network like this:

```
A -> B -> ... -> C -> D -> A
```

A is the start node, D is the stop node. This is 
only relevant at the beginning, since the stop node
does not immediately connect to the start node

Each node can send a `HI` message around the ring.

the start node can send a `ST` (start) message, which
is sent down the line to indicate to the end node
that it is okay to connect to the start node to 
finish the ring.

In order for this to work properly, the nodes must be created
in reverse order: `D, C, ..., B, A`

## Usage

`ring.py` is used as follows:
`./ring.py <input_port> <output_port> <node_id> (start|end|reg)`

where:
* `input_port` is the input TCP port number (on localhost)
* `output_port` is the output TCP port number (on localhost)
* `node_id` is an id number for this node in the range 0 - 255 (inclusive)
* choose:
  * `start` -- start node
  * `end` -- end node
  * `reg` -- regular node

## Examples

run each command in a different terminal or tmux pane,
all on the same host, and in this order:
1. `./ring.py 10003 10001 3 end`
2. `./ring.py 10002 10003 2 reg`
3. `./ring.py 10001 10002 1 start`

This will connect the following:
`Node 1 (10001) -> Node 2 (10002) -> Node 3 (10003)`

You could also ommit the regular node:
1. `./ring.py 10002 10001 2 end`
2. `./ring.py 10001 10002 1 start`

Adding extra regular nodes:
1. `./ring.py 10005 10001 3 end`
2. `./ring.py 10004 10005 4 reg`
3. `./ring.py 10003 10004 3 reg`
4. `./ring.py 10002 10003 2 reg`
5. `./ring.py 10001 10002 1 start`




