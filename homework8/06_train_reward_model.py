import argparse, os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments
from trl import PairwiseRewardTrainer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=str, default="data/reward_data.jsonl")
    ap.add_argument("--model_name", type=str, default="microsoft/deberta-v3-base")
    ap.add_argument("--out", type=str, default="reward_model")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--batch", type=int, default=8)
    args = ap.parse_args()

    ds = load_dataset("json", data_files=args.data, split="train")
    tok = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_name, num_labels=1)

    def tokenize_fn(ex):
        chosen = tok(ex["chosen"], truncation=True, padding="max_length", max_length=512)
        rejected = tok(ex["rejected"], truncation=True, padding="max_length", max_length=512)
        return {
            "input_ids_chosen": chosen["input_ids"],
            "attention_mask_chosen": chosen["attention_mask"],
            "input_ids_rejected": rejected["input_ids"],
            "attention_mask_rejected": rejected["attention_mask"],
        }

    ds = ds.map(tokenize_fn, batched=True, remove_columns=ds.column_names)

    args_tr = TrainingArguments(
        output_dir=args.out,
        per_device_train_batch_size=args.batch,
        num_train_epochs=args.epochs,
        evaluation_strategy="no",
        save_strategy="epoch",
        logging_steps=10,
        fp16=True,
        report_to=[],
    )

    trainer = PairwiseRewardTrainer(
        model=model,
        args=args_tr,
        train_dataset=ds,
        tokenizer=tok,
    )
    trainer.train()
    trainer.save_model(args.out)
    print("Saved reward model to", args.out)

if __name__ == "__main__":
    main()
