Download a dataset from reddit/r/worldnews

```
python src/download_reddit_dataset.py --examples 10000
```
 
Split the data in train/validation (9500 training, 500 validation)

```
split -l 9500 examples_reddit.txt dataset_
```

Transform the datasets to tf-records

```
python tf-serving/tf_models/textsum/data_convert_example.py --command text_to_binary --in_file dataset_aa --out_file train.tf
python tf-serving/tf_models/textsum/data_convert_example.py --command text_to_binary --in_file dataset_ab --out_file validation.tf
```

Train the model:

```
python tf-serving/tf_models/textsum/seq2seq_attention.py \
                                      --mode=train \
                                      --article_key=article \
                                      --abstract_key=abstract \
                                      --data_path=train.tf \
                                      --vocab_path=vocabulary.txt \
                                      --log_root=log \
                                      --train_dir=model
```



python src/download_reddit_dataset.py --examples 100
split -l 95 examples_reddit.txt dataset_
python tf-serving/tf_models/textsum/data_convert_example.py --command text_to_binary --in_file dataset_aa --out_file train.tf
python tf-serving/tf_models/textsum/data_convert_example.py --command text_to_binary --in_file dataset_ab --out_file validation.tf
python tf-serving/tf_models/textsum/seq2seq_attention.py --mode=train --article_key=article --abstract_key=abstract --data_path=train.tf --vocab_path=vocabulary.txt --log_root=log --train_dir=model


python tf-serving/tf_models/textsum/seq2seq_attention.py --mode=train --article_key=article --abstract_key=abstract --data_path=tf-serving/tf_models/textsum/data/data --vocab_path=tf-serving/tf_models/textsum/data/vocab --log_root=log --train_dir=model





python tf-serving/tf_models/textsum/seq2seq_attention.py --mode=train --article_key=article --abstract_key=abstract --data_path=tf-serving/tf_models/textsum/data/data --vocab_path=tf-serving/tf_models/textsum/data/vocab --log_root=log --train_dir=model
python tf-serving/tf_models/textsum/seq2seq_attention.py --mode=eval --article_key=article --abstract_key=abstract --data_path=tf-serving/tf_models/textsum/data/data --vocab_path=tf-serving/tf_models/textsum/data/vocab --log_root=log --eval_dir=eval

bazel-bin/textsum/seq2seq_attention \
  --mode=eval \
  --article_key=article \
  --abstract_key=abstract \
  --data_path=data/validation-* \
  --vocab_path=data/vocab \
  --log_root=textsum/log_root \
  --eval_dir=textsum/log_root/eval