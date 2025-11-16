import gleam/erlang/process
import gleam/int
import gleam/io

pub type InetBackend {
  InetBackend
}

pub type ListenOption {
  ListenOption
}

pub type ListenOptionUnion {
  AnInetBackend(InetBackend)
  AListenOption(ListenOption)
}

pub type Socket {
  Socket
}

@external(erlang, "listen_tcp", "listen_tcp")
pub fn listen_tcp(port: Int) -> Result(Socket, String)

@external(erlang, "gen_tcp", "accept")
pub fn accept(lsock: Socket) -> Result(Socket, String)

@external(erlang, "gen_tcp", "recv")
pub fn recv(sock: Socket, length: Int) -> Result(String, String)

@external(erlang, "gen_tcp", "send")
pub fn send(sock: Socket, packet: String) -> Result(Nil, String)

@external(erlang, "gen_tcp", "close")
pub fn close(sock: Socket) -> Nil

fn on_accept(sock: Socket) {
  let recv_res = recv(sock, 0)
  case recv_res {
    Ok(p) -> {
      let send_res = send(sock, p)
      case send_res {
        Error(_) -> {
          close(sock)
        }
        // ok atom not compatible with gleam
        _ -> {
          let _ = on_accept(sock)
          Nil
        }
      }
    }
    Error(_) -> {
      close(sock)
    }
  }

  Nil
}

fn run_server_loop(lsock: Socket) {
  let sock = accept(lsock)
  case sock {
    Ok(s) -> {
      process.spawn(fn() { on_accept(s) })
      Nil
    }
    Error(_e) -> io.println("Failed to accept connection...")
  }
  run_server_loop(lsock)
}

pub fn main() {
  let port = 6969
  case listen_tcp(port) {
    Ok(lsock) -> {
      io.println("Listening on port " <> int.to_string(port))
      run_server_loop(lsock)
      Nil
    }
    Error(_reason) -> {
      io.println("Could not listen on port " <> int.to_string(port))
      Nil
    }
  }
}
