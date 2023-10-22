use std::io::Read;
use sha2::{Sha256, Digest};
use wasm_bindgen::prelude::*;
use hex;

const BLOCK_SIZE: usize = 128; // 1024 bits = 128 bytes

// Compute the Merkle root of a list of hashes
fn compute_merkle_root(mut hashes: Vec<Vec<u8>>) -> Vec<u8> {
    while hashes.len() > 1 {
        let mut parents = Vec::new();
        while let Some(left_child) = hashes.pop() {
            if let Some(right_child) = hashes.pop() {
                let mut hasher = Sha256::new();
                hasher.input(&left_child);
                hasher.input(&right_child);
                parents.push(hasher.result().to_vec());
            } else {
                parents.push(left_child);
            }
        }
        hashes = parents;
    }
    hashes[0].clone()
}

#[wasm_bindgen]
pub fn compute_file_merkle_root(file_path: &str) -> String {
    let mut file = std::fs::File::open(file_path).unwrap();
    let mut blocks = Vec::new();
    let mut buffer = [0u8; BLOCK_SIZE];
    while let Ok(bytes_read) = file.read(&mut buffer) {
        if bytes_read == 0 {
            break;
        }
        let hash = Sha256::digest(&buffer[0..bytes_read]).to_vec();
        blocks.push(hash);
    }
    let merkle_root= compute_merkle_root(blocks);
    hex::encode(merkle_root)
}
