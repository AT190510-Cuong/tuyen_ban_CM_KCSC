const { Sequelize, DataTypes } = require("sequelize");
const config = require("./config");

const sequelize = new Sequelize(config.DATABASE_URL, {
    dialect: "postgres",
    logging: false,
});

const User = sequelize.define(
    "User",
    {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
            allowNull: false,
        },
        username: {
            type: DataTypes.STRING,
            unique: true,
            allowNull: false,
        },
        hashed_password: {
            type: DataTypes.STRING,
            allowNull: false,
        },
    },
    {
        tableName: "users",
        timestamps: false,
    }
);

async function getUserByUsername(username) {
    return await User.findOne({ where: { username } });
}

async function createUser(userData) {
    return await User.create(userData);
}

async function initDB() {
    try {
        await sequelize.sync({ alter: true });
        console.log("Database & tables created!");
    } catch (error) {
        console.error("Unable to connect to the database:", error);
    }
}

function getDB() {
    return {
        getUserByUsername,
        createUser,
        sequelize,
    };
}

module.exports = {
    User,
    sequelize,
    initDB,
    getUserByUsername,
    createUser,
    getDB,
};
