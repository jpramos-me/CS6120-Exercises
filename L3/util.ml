open Core
open Yojson

(** split_blocks json takes a Bril generated JSON file
    and gets the set of instructions and outputs the list
    of blocks. *)
let split_blocks json = 
  match 