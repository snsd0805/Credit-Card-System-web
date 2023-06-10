
CREATE TABLE "shops" (
	"id"	INTEGER,
	"address"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

---------------------------------------------------

CREATE TABLE "products" (
	"id"	INTEGER,
	"shop_id"	INTEGER,
	"name"	TEXT,
	"code"	TEXT,
	"price"	INTEGER,
	FOREIGN KEY("shop_id") REFERENCES "shops"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

---------------------------------------------------

CREATE TABLE "orders" (
	"id"	INTEGER,
	"shop_id"	INTEGER,
	"client_addr"	TEXT,
	"amount"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("shop_id") REFERENCES "shops"("id")
);

---------------------------------------------------

CREATE TABLE "order_products" (
	"id"	INTEGER,
	"order_id"	INTEGER,
	"product_id"	INTEGER,
	"count"	INTEGER,
	FOREIGN KEY("product_id") REFERENCES "products"("id"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("order_id") REFERENCES "orders"("id")
);

---------------------------------------------------

INSERT INTO "main"."shops"("id","address","name") VALUES (NULL,"0x73D081e82b35D6E6f9f5e72EBBB6b637d4f46992","全家便利商店");
INSERT INTO "main"."shops"("id","address","name") VALUES (NULL,"0xDa68136fcB885a2ec44db6dcE946F656aF457A76","暨大圖文部");

INSERT INTO "main"."products"("id","shop_id","name","code", "price") VALUES (NULL,1,"濃辛咖哩飯","7233957360139", "10000000000000000");
INSERT INTO "main"."products"("id","shop_id","name","code", "price") VALUES (NULL,1,"霜淇淋","4718022345288", "5000000000000000");
INSERT INTO "main"."products"("id","shop_id","name","code", "price") VALUES (NULL,2,"證件套","748009345271", "25000000000000000");
INSERT INTO "main"."products"("id","shop_id","name","code", "price") VALUES (NULL,2,"便條紙","4979274503226", "4000000000000000");
