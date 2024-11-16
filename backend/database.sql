-- Criar tabela de cupcakes
CREATE TABLE IF NOT EXISTS cupcakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL
);

-- Inserir dados iniciais de cupcakes
INSERT INTO cupcakes (nome, descricao, preco) VALUES
    ('Delícia de Chocolate', 'Cupcake de chocolate rico com recheio de ganache', 4.50),
    ('Sonho de Baunilha', 'Clássico cupcake de baunilha com cobertura de buttercream', 3.50),
    ('Veludo Vermelho', 'Cupcake de veludo vermelho suave com cobertura de cream cheese', 4.75),
    ('Raspas de Limão', 'Cupcake de limão refrescante com creme de limão', 4.00),
    ('Caramelo Crocante', 'Cupcake com infusão de caramelo e cobertura crocante', 4.25),
    ('Campos de Morango', 'Cupcake de morango fresco com geleia de morango', 4.50),
    ('Paraíso de Coco', 'Cupcake com sabor de coco e flocos de coco na cobertura', 4.00),
    ('Dose de Espresso', 'Cupcake de mocha com buttercream de espresso', 4.75),
    ('Frescura de Menta', 'Cupcake de chocolate com toque de menta', 4.50),
    ('Amendoim com Chocolate', 'Cupcake de amendoim com cobertura de chocolate', 4.75),
    ('Cookies e Creme', 'Cupcake clássico recheado com Oreo', 4.25),
    ('Especiarias de Abóbora', 'Cupcake sazonal de abóbora com especiarias', 4.00),
    ('Explosão de Mirtilo', 'Cupcake de mirtilo com cobertura de creme de mirtilo', 4.25),
    ('Maple com Noz Pecan', 'Cupcake com sabor de maple e cobertura de nozes pecan', 4.75),
    ('Choco-Berry', 'Cupcake de chocolate com cobertura de framboesa', 4.50),
    ('Caramelo Salgado', 'Cupcake de caramelo salgado com recheio cremoso de caramelo', 4.50),
    ('Alegria de Amêndoa', 'Cupcake com sabor de amêndoa e fatias de amêndoa na cobertura', 4.25),
    ('Bomba de Cereja', 'Cupcake de cereja com recheio de geleia de cereja', 4.00),
    ('Banana Split', 'Cupcake de banana com cobertura de chocolate', 4.50),
    ('Paraíso de Avelã', 'Cupcake de chocolate com avelã', 4.75);

-- Criar tabela de carrinho
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cupcake_id INTEGER NOT NULL,
    FOREIGN KEY (cupcake_id) REFERENCES cupcakes (id)
);

-- Criar tabela de pedidos
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
