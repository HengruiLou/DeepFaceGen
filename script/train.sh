export model_names=('xception')
# dataset_names=('dalle1' 'dalle3' 'Baidu' 'SD1' 'img2img' 'Midjourney' 'OJ' 'pix2pix' 'SD2' 'SDXL' 'variations' 'tra_ATVG-Net' 'tra_BlendFace' 'tra_DeepFakes' 'tra_DeepFakes-StarGAN-Stack' 'tra_DiscoFaceGAN' 'tra_FaceShifter' 'tra_FOMM' 'tra_FSGAN' 'tra_MaskGAN' 'tra_MMReplacement' 'tra_SC-FEGAN' 'tra_StarGAN' 'tra_StarGAN2' 'tra_StyleGAN2' 'tra_Talking_Head')
dataset_names=('tra_ATVG-Net' 'tra_BlendFace' 'tra_DeepFakes' 'tra_DeepFakes-StarGAN-Stack' 'tra_DiscoFaceGAN' 'tra_FaceShifter' 'tra_FOMM' 'tra_FSGAN' 'tra_MaskGAN' 'tra_MMReplacement' 'tra_SC-FEGAN' 'tra_StarGAN' 'tra_StarGAN2' 'tra_StyleGAN2' 'tra_Talking_Head')
export device='cuda:0'

# proxychains4 python ../train.py \4

for model_name in "${model_names[@]}"
do
    for dataset_name in "${dataset_names[@]}"

    do
        echo "Processing tar_dataset: $tar_dataset"

        python ../train.py \
            --model_name ${model_name} \
            --dataset_name ${dataset_name} \
            --device ${device}
        
        echo "-----------------------------"

    done
done