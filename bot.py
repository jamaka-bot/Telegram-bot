async def kirim_miqdor(message: types.Message, state: FSMContext):
    await state.update_data(miqdor=float(message.text))
    await Kirim.izoh.set()
    await message.answer("Izoh kiriting (yoki - yozing):")

@dp.message_handler(state=Kirim.izoh)
async def kirim_izoh(message: types.Message, state: FSMContext):
    data = await state.get_data()
    db.kirim(data['mahsulot_id'], data['miqdor'], message.text)
    await state.finish()
    await message.answer("✅ Kirim qayd etildi!", reply_markup=asosiy_tugmalar())

@dp.message_handler(text="📤 Chiqim")
async def chiqim_start(message: types.Message):
    data = db.mahsulotlar_royxat()
    if not data:
        await message.answer("Mahsulot yo'q.")
        return
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for m in data:
        kb.add(f"{m[0]}. {m[1]}")
    await Chiqim.mahsulot.set()
    await message.answer("Qaysi mahsulotdan chiqim?", reply_markup=kb)

@dp.message_handler(state=Chiqim.mahsulot)
async def chiqim_mahsulot(message: types.Message, state: FSMContext):
    mahsulot_id = int(message.text.split('.')[0])
    await state.update_data(mahsulot_id=mahsulot_id)
    await Chiqim.miqdor.set()
    await message.answer("Miqdorni kiriting:")

@dp.message_handler(state=Chiqim.miqdor)
async def chiqim_miqdor(message: types.Message, state: FSMContext):
    await state.update_data(miqdor=float(message.text))
    await Chiqim.izoh.set()
    await message.answer("Izoh kiriting (yoki - yozing):")

@dp.message_handler(state=Chiqim.izoh)
async def chiqim_izoh(message: types.Message, state: FSMContext):
    data = await state.get_data()
    db.chiqim(data['mahsulot_id'], data['miqdor'], message.text)
    await state.finish()
    await message.answer("✅ Chiqim qayd etildi!", reply_markup=asosiy_tugmalar())

@dp.message_handler(text="📊 Hisobot")
async def hisobot(message: types.Message):
    data = db.mahsulotlar_royxat()
    if not data:
        await message.answer("Ma'lumot yo'q.")
        return
    jami = sum(m[4]*m[5] for m in data)
    text = f"📊 Hisobot:\nJami mahsulot: {len(data)} ta\nUmumiy qiymat: {jami:,.0f} so'm"
    await message.answer(text)

@dp.message_handler(text="⚠️ Kam qolganlar")
async def kam_qolganlar(message: types.Message):
    data = db.kam_qolganlar()
    if not data:
        await message.answer("✅ Hamma mahsulot yetarli!")
        return
    text = "⚠️ Kam qolgan mahsulotlar:\n\n"
    for m in data:
        text += f"• {m[1]}: {m[4]} {m[3]}\n"
    await message.answer(text)

@dp.message_handler(text="📋 Harakatlar tarixi")
async def tarix(message: types.Message):
    data = db.harakatlar_tarixi()
    if not data:
        await message.answer("Tarix bo'sh.")
        return
    text = "📋 Oxirgi harakatlar:\n\n"
    for h in data:
        text += f"• {h[0][:10]} | {h[1]} | {h[2]} | {h[3]}\n"
    await message.answer(text)

if name == '__main__':
    executor.start_polling(dp, skip_updates=True)
