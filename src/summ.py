import tensorflow as tf
import sys
sys.path.append('tf-serving/tf_models/textsum')
import seq2seq_attention_model
import data

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--content', metavar='content', )
    args = parser.parse_args()
    hps = seq2seq_attention_model.HParams(
        mode='eval',  # train, eval, decode
        min_lr=0.01,  # min learning rate.
        lr=0.15,  # learning rate
        batch_size=1,
        enc_layers=4,
        enc_timesteps=120,
        dec_timesteps=30,
        min_input_len=2,  # discard articles/summaries < than this
        num_hidden=256,  # for rnn cell
        emb_dim=128,  # If 0, don't use embedding
        max_grad_norm=2,
        num_softmax_samples=4096)

    vocab = data.Vocab('vocabulary.txt', 1000000)
    model = seq2seq_attention_model.Seq2SeqAttentionModel(hps, vocab, num_gpus=0)
    model.build_graph()
    saver = tf.train.Saver()
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    ckpt_state = tf.train.get_checkpoint_state('model_save')
    (summaries, loss, train_step) = model.run_eval_step(
        sess, [args.content], [''], targets, article_lens,
        abstract_lens, loss_weights)