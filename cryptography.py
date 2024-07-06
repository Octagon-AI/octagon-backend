import os
import torch
import json
import torch.nn as nn
import ezkl
import asyncio


async def compile_prover(id, shape):
    model_path = os.path.join('models', id, 'model.onnx')
    compiled_model_path = os.path.join('models', id, 'model.compiled')
    pk_path = os.path.join('models', id, 'test.pk')
    vk_path = os.path.join('models', id, 'test.vk')
    settings_path = os.path.join('models', id, 'settings.json')
    witness_path = os.path.join('models', id, 'witness.json')
    data_path = os.path.join('models', id, 'input.json')
    srs_path = os.path.join('models', id, 'kzg.srs')
    proof_path = os.path.join('models', id, 'test.pf')
    cal_path = os.path.join('models', id, "calibration.json")



    py_run_args = ezkl.PyRunArgs()
    py_run_args.input_visibility = "private"
    py_run_args.output_visibility = "public"
    py_run_args.param_visibility = "private" # private by default

    res = ezkl.gen_settings(model_path, settings_path, py_run_args=py_run_args)
    assert res == True

    data_array = (torch.rand(20, *shape, requires_grad=True).detach().numpy()).reshape([-1]).tolist()
    data = dict(input_data = [data_array])
    json.dump(data, open(cal_path, 'w'))

    await ezkl.calibrate_settings(cal_path, model_path, settings_path, "resources")

    res = ezkl.compile_circuit(model_path, compiled_model_path, settings_path)
    assert res == True

    # srs path
    res = await ezkl.get_srs(settings_path=settings_path, srs_path=srs_path)
    assert res == True

    return "Model compiled"


async def prove_inference(id, x):
    # raw_model_path = os.path.join("models", id, "model.pth")
    # if not os.path.exists(raw_model_path):
    #     return 'Model not found'
    
    # print("path", raw_model_path)

    # import pickle
    # circuit = dill.load(open("models/12345/model.pkl", 'rb'))
    # circuit = torch.load(raw_model_path)

    model_path = os.path.join('models', id, 'model.onnx')
    compiled_model_path = os.path.join('models', id, 'model.compiled')
    pk_path = os.path.join('models', id, 'test.pk')
    vk_path = os.path.join('models', id, 'test.vk')
    settings_path = os.path.join('models', id, 'settings.json')
    witness_path = os.path.join('models', id, 'witness.json')
    data_path = os.path.join('models', id, 'input.json')
    srs_path = os.path.join('models', id, 'kzg.srs')
    proof_path = os.path.join('models', id, 'test.pf')
    
    data_array = ((x.squeeze(1)).detach().numpy()).reshape([-1]).tolist() 
    data = dict(input_data = [data_array])

    # Serialize data into file:
    json.dump(data, open(data_path, 'w'))

    res = await ezkl.gen_witness(data_path, compiled_model_path, witness_path)
    assert os.path.isfile(witness_path)

    res = ezkl.setup(
            compiled_model_path,
            vk_path,
            pk_path,
            srs_path,
        )

    assert res == True
    assert os.path.isfile(vk_path)
    assert os.path.isfile(pk_path)
    assert os.path.isfile(settings_path)
    assert os.path.isfile(srs_path)

    proof = ezkl.prove(
            witness_path,
            compiled_model_path,
            pk_path,
            proof_path,

            "single",
            srs_path,
        )
    # print(proof)
    assert os.path.isfile(proof_path)

    # VERIFY IT

    res = ezkl.verify(
            proof_path,
            settings_path,
            vk_path,
            srs_path,
        )

    assert res == True

    onchain_input_array = []
    for i, value in enumerate(proof["instances"]):
        for j, field_element in enumerate(value):
            onchain_input_array.append(ezkl.felt_to_big_endian(field_element))

    return {"inputs": onchain_input_array, "proof": proof['proof']}


if __name__ == '__main__':
    x = torch.tensor([[[0.8790, 0.6273, 0.2377, 0.5785, 0.9947, 0.9937, 0.5818, 0.6087,
          0.6087, 0.6312]]])
    res = asyncio.run(compile_prover('12345', x.shape))
    print(res)

    res = asyncio.run(prove_inference('12345', x))
    print(res)
